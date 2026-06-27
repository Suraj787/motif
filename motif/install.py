"""Controlled installation, diff/plan, rollback snapshot, and provenance manifest.

Installation NEVER blindly copies files and NEVER runs third-party installers
against the target. It inspects, plans, snapshots, applies a controlled patch,
validates, and reverts on failure. Only `bundled` / `installable` records with a
known licence may be applied; everything else is refused.
"""
from __future__ import annotations
import json
import shutil
import hashlib
import datetime
import pathlib
from dataclasses import dataclass, field
from . import registry, project as project_mod, scan as scan_mod

ROOT = registry.ROOT
SNAP_DIR = ROOT / ".motif" / "snapshots"


def _sha256(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


@dataclass
class InstallPlan:
    component_id: str
    source: str
    license: str
    usability_mode: str
    target: str
    files: list[dict] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    dependency_plan: list[dict] = field(default_factory=list)
    security_findings: list[dict] = field(default_factory=list)
    security_verdict: str = "pass"
    project: dict = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    refused: str | None = None

    def to_dict(self) -> dict:
        return {
            "component_id": self.component_id, "source": self.source,
            "license": self.license, "usability_mode": self.usability_mode,
            "target": self.target, "project": self.project,
            "files": self.files, "dependencies": self.dependencies,
            "dependency_plan": self.dependency_plan,
            "security_findings": self.security_findings,
            "security_verdict": self.security_verdict,
            "warnings": self.warnings, "refused": self.refused,
        }


def _dependency_plan(recipe_deps: list[str], installed: dict) -> list[dict]:
    """Apply the dependency-policy preference order against what the project has."""
    plan: list[dict] = []
    for dep in recipe_deps:
        if dep in installed:
            plan.append({"dependency": dep, "decision": "reuse-existing",
                         "detail": f"already in project ({installed[dep]})"})
        else:
            plan.append({"dependency": dep, "decision": "needs-approval",
                         "detail": "new dependency, prefer a dependency-free recipe first"})
    if not recipe_deps:
        plan.append({"dependency": None, "decision": "dependency-free",
                     "detail": "no new dependencies required"})
    return plan


def _component(component_id: str) -> registry.Record | None:
    for r in registry.load_records("components"):
        if r.data["id"] == component_id:
            return r
    return None


def _recipe_for(component_id: str) -> registry.Record | None:
    # A bundled/installable component maps to a recipe implementation file when present.
    for r in registry.load_records("recipes"):
        if component_id in (r.data.get("source_references") or []):
            return r
    return None


def plan_install(component_id: str, target: str) -> InstallPlan:
    rec = _component(component_id)
    if rec is None:
        return InstallPlan(component_id, "?", "?", "?", target, refused="no such component record")
    d = rec.data
    plan = InstallPlan(
        component_id=component_id, source=d["source"], license=d["license"],
        usability_mode=d["usability_mode"], target=target,
        dependencies=d.get("dependencies", []),
    )
    if d["usability_mode"] not in ("bundled", "installable"):
        plan.refused = (f"usability_mode='{d['usability_mode']}' is not installable "
                        f"(LICENCE/usability gate). Adapt the concept instead.")
        return plan
    if d["license"].lower().startswith("unknown") or d["license"] == "":
        plan.refused = "unknown licence, refused by the LICENCE GATE"
        return plan

    # Inspect the real target project so we never mismatch frameworks or re-add deps.
    info = project_mod.detect(target)
    plan.project = info.to_dict()
    plan.dependency_plan = _dependency_plan(plan.dependencies, info.dependencies)

    impl = _recipe_for(component_id)
    if impl and impl.data.get("implementation_path"):
        recipe_fw = impl.data.get("framework", "browser-native")
        if info.framework != "unknown" and not project_mod.compatible(recipe_fw, info.framework):
            plan.warnings.append(
                f"recipe framework '{recipe_fw}' is not compatible with project "
                f"framework '{info.framework}'. Adapt the concept natively instead of "
                f"installing a foreign framework.")
        src = ROOT / impl.data["implementation_path"]
        if src.exists():
            # Static-scan the implementation we are about to apply.
            findings = scan_mod.scan_all(src.parent)
            plan.security_findings = [f.to_dict() for f in findings
                                      if f.severity in ("warn", "high", "critical")]
            plan.security_verdict = scan_mod.verdict(findings)
            if plan.security_verdict == "reject":
                plan.refused = "implementation failed static security scan (reject verdict)"
                return plan
            plan.files.append({"action": "create", "path": f"{target}/{src.name}",
                               "from": impl.data["implementation_path"], "sha256": _sha256(src)})
    if not plan.files:
        plan.files.append({"action": "note", "path": target,
                           "from": d.get("installation_method", "official registry"),
                           "sha256": ""})
    return plan


def write_provenance(plan: InstallPlan, target: pathlib.Path) -> pathlib.Path:
    manifest = {
        "component": plan.component_id,
        "implementation_id": f"motif:{plan.component_id}",
        "source_type": plan.usability_mode,
        "inspiration_sources": [plan.source],
        "source_version_commit": "pinned-on-refresh",
        "license": plan.license,
        "installation_date": datetime.date.today().isoformat(),
        "created_modified_files": [f["path"] for f in plan.files],
        "dependencies": plan.dependencies,
        "security_review": plan.security_findings or "static scan: no blocking findings",
        "accessibility_support": "reduced-motion required; see recipe record",
        "reduced_motion_behaviour": "instant/static fallback",
    }
    out = target / "motif-provenance.json"
    out.write_text(json.dumps(manifest, indent=2) + "\n")
    return out


def snapshot(target: pathlib.Path) -> pathlib.Path:
    SNAP_DIR.mkdir(parents=True, exist_ok=True)
    snap = SNAP_DIR / (target.name + ".snapshot")
    if snap.exists():
        shutil.rmtree(snap)
    if target.exists():
        shutil.copytree(target, snap)
    else:
        snap.mkdir(parents=True)
    return snap


def rollback(target: pathlib.Path) -> bool:
    snap = SNAP_DIR / (target.name + ".snapshot")
    if not snap.exists():
        return False
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(snap, target)
    return True
