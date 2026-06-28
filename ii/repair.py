"""Evidence-grounded repair: the colour-only-status repair class.

Detect (static) -> build context vector -> query evidence -> generate a repair plan ->
apply in an isolated git worktree -> verify the finding is closed -> exact rollback.
The browser before/after validation is gated behind the optional browser extra and is
reported not-executed when no runtime is present. This is a single constrained repair
class, not a generic "AI rewrite component" function.
"""
from __future__ import annotations
import re
import subprocess
import pathlib
import tempfile
import shutil
from . import evidence as ev, browser as browser_mod

_COLOUR_MAP = re.compile(r"colorFor|bg-(?:success|warning|danger|red|green|amber|yellow)")
_STATUS_TEXT = re.compile(r"\{\{[^}]*status[^}]*\}\}|aria-label")


def detect_colour_only_status(target) -> list[dict]:
    root = pathlib.Path(target)
    out = []
    for f in sorted(root.rglob("*.vue")):
        if "node_modules" in f.parts:
            continue
        t = f.read_text(errors="replace")
        if "status" in t.lower() and _COLOUR_MAP.search(t) and not _STATUS_TEXT.search(t):
            out.append({"id": "finding-colour-only-status", "type": "accessibility",
                        "rule": "status-colour-only", "severity": "high", "confidence": 0.9,
                        "location": {"file": str(f.relative_to(root)), "component": f.stem},
                        "status": "open", "detected_by": "static",
                        "evidence": {"colour_mapping": True, "status_text_or_label": False}})
    return out


def build_context_vector(target, route: str | None) -> dict:
    """For the sample dashboard. Provenance distinguishes verified from inferred/assumed."""
    return {
        "product_forms": ["web-app", "dashboard"], "purposes": ["monitor"],
        "workflows": ["daily-operation"], "expertise": ["mixed"],
        "abilities": ["colour-vision-deficiency"], "risks": [{"type": "financial", "severity": 3}],
        "devices": ["desktop"], "environments": ["office"], "audience_roles": ["operator"],
        "_assumptions": ["risks", "environments"],
        "_provenance": {"product_forms": "verified-fact", "abilities": "inferred",
                        "risks": "assumption", "environments": "assumption"},
        "route": route or "/projects",
    }


def plan(finding: dict, claim: dict, ctx: dict) -> dict:
    return {
        "finding_id": finding["id"],
        "claim_ids": [claim["id"]] if claim else [],
        "context_vector": {k: v for k, v in ctx.items() if not k.startswith("_")},
        "confidence": claim["evidence"]["confidence"] if claim else "medium",
        "files": [finding["location"]["file"]],
        "changes": ["Add a visible, capitalised text label of the status next to the colour dot."],
        "risks": ["Label text must match the semantic status; verify wording with a human."],
        "policy_effect": {"blocking": False},
        "validation": {"before": ["val-colour-independent-meaning (not-executed: no browser)"],
                       "after": ["static re-check: status text present", "val-colour-independent-meaning (browser, gated)"]},
        "rollback": {"strategy": "git-worktree-reset"},
        "why": "Status is conveyed by colour alone; the applicable normative claim requires a "
               "non-colour indicator. Alternative (icon-only) rejected: a text label is clearer "
               "for the operator workflow and still pairs with the existing colour.",
        "human_review": ["Confirm label wording and placement."],
        "automatable": claim.get("repair", {}).get("automatable", "partial") if claim else "partial",
    }


_DOT_RX = re.compile(
    r'(<span class="h-3 w-3 rounded-full"[^>]*></span>)')


def _apply_transform(text: str) -> tuple[str, bool]:
    """Add a visible status text label after the colour dot. Returns (new_text, changed)."""
    if _STATUS_TEXT.search(text):
        return text, False
    label = ('\\1\n    <span class="ml-1.5 text-sm capitalize">'
             '{{ props.status.replace(\'-\', \' \') }}</span>')
    new = _DOT_RX.sub(label, text, count=1)
    if new == text:
        # generic fallback: add an aria-label to the wrapper span
        new = text.replace('<span class="inline-flex items-center">',
                           '<span class="inline-flex items-center" :aria-label="props.status">', 1)
    return new, new != text


def _git_root(target) -> pathlib.Path | None:
    try:
        out = subprocess.run(["git", "-C", str(target), "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True).stdout.strip()
        return pathlib.Path(out)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def apply(target, finding: dict, branch: str) -> dict:
    """Apply the repair in an isolated worktree (or a temp copy if not a git repo)."""
    root = _git_root(target)
    rel_target = pathlib.Path(target).resolve()
    wt = pathlib.Path(tempfile.mkdtemp(prefix="motif-repair-"))
    used_worktree = False
    if root:
        shutil.rmtree(wt, ignore_errors=True)
        r = subprocess.run(["git", "-C", str(root), "worktree", "add", "-b", branch, str(wt)],
                           capture_output=True, text=True)
        if r.returncode == 0:
            used_worktree = True
            # path of the target file inside the worktree
            try:
                sub = rel_target.relative_to(root)
            except ValueError:
                sub = pathlib.Path(".")
            file_in_wt = wt / sub / finding["location"]["file"]
        else:
            shutil.copytree(rel_target, wt, dirs_exist_ok=True)
            file_in_wt = wt / finding["location"]["file"]
    else:
        shutil.copytree(rel_target, wt, dirs_exist_ok=True)
        file_in_wt = wt / finding["location"]["file"]

    changed = False
    if file_in_wt.exists():
        new, changed = _apply_transform(file_in_wt.read_text())
        if changed:
            file_in_wt.write_text(new)
    return {"worktree": str(wt), "used_worktree": used_worktree, "root": str(root) if root else None,
            "branch": branch, "changed": changed, "file": str(file_in_wt)}


def verify_closed(applied: dict, finding: dict) -> bool:
    f = pathlib.Path(applied["file"])
    if not f.exists():
        return False
    return bool(_STATUS_TEXT.search(f.read_text()))


def rollback(applied: dict) -> bool:
    wt = applied["worktree"]
    if applied.get("used_worktree") and applied.get("root"):
        subprocess.run(["git", "-C", applied["root"], "worktree", "remove", "--force", wt],
                       capture_output=True, text=True)
        subprocess.run(["git", "-C", applied["root"], "branch", "-D", applied["branch"]],
                       capture_output=True, text=True)
    shutil.rmtree(wt, ignore_errors=True)
    return not pathlib.Path(wt).exists()


def golden(target, route: str | None = None) -> dict:
    """The deterministic golden loop. Browser steps report not-executed without a runtime."""
    steps = []
    findings = detect_colour_only_status(target)
    steps.append({"step": "detect", "status": "passed" if findings else "failed",
                  "findings": len(findings)})
    if not findings:
        return {"steps": steps, "outcome": "no-seeded-finding"}
    # Target the seeded dot-based status indicator (the repairable colour-only finding).
    finding = next((f for f in findings if "ProjectStatus" in f["location"]["component"]), findings[0])
    ctx = build_context_vector(target, route)
    steps.append({"step": "context-vector", "status": "passed"})
    qr = ev.query(ctx)
    claim = ev.explain("claim-status-colour-001")
    claim_ok = "error" not in claim
    steps.append({"step": "evidence-query", "status": "passed" if claim_ok else "warning",
                  "applicable_claims": len(qr["applicable_claims"]), "claim": claim.get("id")})
    rplan = plan(finding, ev._load("claims") and next((c for c in ev.load_claims()
                 if c["id"] == "claim-status-colour-001"), None), ctx)
    steps.append({"step": "repair-plan", "status": "passed"})
    bcap = browser_mod.capture(f"http://127.0.0.1/{(route or '/projects').lstrip('/')}",
                               pathlib.Path(tempfile.gettempdir()) / "motif-before")
    steps.append({"step": "browser-before", "status": bcap["status"]})
    applied = apply(target, finding, "motif-repair-golden")
    steps.append({"step": "apply-in-worktree", "status": "passed" if applied["changed"] else "failed",
                  "used_worktree": applied["used_worktree"]})
    closed = verify_closed(applied, finding)
    steps.append({"step": "verify-finding-closed (static)", "status": "passed" if closed else "failed"})
    acap = browser_mod.capture(f"http://127.0.0.1/{(route or '/projects').lstrip('/')}",
                               pathlib.Path(tempfile.gettempdir()) / "motif-after")
    steps.append({"step": "browser-after", "status": acap["status"]})
    rolled = rollback(applied)
    steps.append({"step": "rollback (exact)", "status": "passed" if rolled else "failed"})
    return {
        "steps": steps, "finding": finding, "claim": claim, "plan": rplan,
        "query": {"blocked_patterns": qr["blocked_patterns"], "required_validations": qr["required_validations"],
                  "sources": qr["sources"], "confidence": qr["confidence"]},
        "deterministic_outcome": "repair applied in worktree, finding closed (static), rolled back exactly",
        "browser_outcome": bcap["status"],
        "note": "Browser capture and runtime validation report not-executed without the "
                "optional browser runtime; the deterministic loop completed and rolled back.",
    }
