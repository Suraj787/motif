"""Target-project inspection: framework, conventions, installed dependencies.

Used by the controlled installer so a recipe is matched to the project's real
framework and existing dependencies (never installing one framework to get an
effect for another, never adding a dependency the project already has).
"""
from __future__ import annotations
import json
import pathlib
from dataclasses import dataclass, field


@dataclass
class ProjectInfo:
    root: str
    framework: str = "unknown"          # react | vue | svelte | angular | frappe-vue | browser-native | unknown
    typescript: bool = False
    tailwind: bool = False
    dependencies: dict = field(default_factory=dict)   # name -> version
    components_dir: str | None = None
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "root": self.root, "framework": self.framework,
            "typescript": self.typescript, "tailwind": self.tailwind,
            "dependency_count": len(self.dependencies),
            "components_dir": self.components_dir, "notes": self.notes,
        }


def _read_json(p: pathlib.Path) -> dict:
    try:
        return json.loads(p.read_text())
    except (OSError, json.JSONDecodeError):
        return {}


def detect(target: str | pathlib.Path) -> ProjectInfo:
    root = pathlib.Path(target)
    info = ProjectInfo(root=str(root))
    pkg = _read_json(root / "package.json")
    deps: dict = {}
    for field_name in ("dependencies", "devDependencies", "peerDependencies"):
        deps.update(pkg.get(field_name, {}) or {})
    info.dependencies = deps

    # framework detection (most specific first)
    has = lambda *names: any(n in deps for n in names)
    is_frappe = (root / "frappe-bench").exists() or has("frappe-ui") or \
        any((root / d).exists() for d in ("apps", "../apps"))
    if has("vue") and is_frappe:
        info.framework = "frappe-vue"
    elif has("@angular/core"):
        info.framework = "angular"
    elif has("svelte"):
        info.framework = "svelte"
    elif has("vue"):
        info.framework = "vue"
    elif has("react", "react-dom"):
        info.framework = "react"
    elif pkg and not deps:
        info.framework = "browser-native"

    info.typescript = (root / "tsconfig.json").exists() or has("typescript")
    info.tailwind = has("tailwindcss") or (root / "tailwind.config.js").exists() or \
        (root / "tailwind.config.ts").exists()

    for cand in ("src/components", "components", "app/components", "src/lib/components"):
        if (root / cand).is_dir():
            info.components_dir = cand
            break

    if info.framework == "unknown":
        info.notes.append("Could not infer framework; pass an explicit framework or inspect manually.")
    return info


# recipe framework -> compatible project frameworks
_COMPAT = {
    "browser-native": {"react", "vue", "svelte", "angular", "frappe-vue", "browser-native", "unknown"},
    "vue": {"vue", "frappe-vue"},
    "frappe-vue": {"frappe-vue", "vue"},
    "react": {"react"},
    "svelte": {"svelte"},
    "angular": {"angular"},
    "vanilla": {"react", "vue", "svelte", "angular", "frappe-vue", "browser-native", "unknown"},
}


def compatible(recipe_framework: str, project_framework: str) -> bool:
    return project_framework in _COMPAT.get(recipe_framework, set())
