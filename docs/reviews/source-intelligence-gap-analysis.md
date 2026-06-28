# Source Intelligence gap analysis

Branch `feat/source-intelligence-v3.1` from `main` (stable `v3.0.0` released). Target version
**v3.1.0** (a new product capability, a minor bump, not a patch).

## Reusable foundations (already in the repo)
- `motif/jsonschema_min.py`, `motif/yaml_min.py`: dependency-free schema validation and a
  restricted YAML reader. The source registry reuses both.
- `ii/evidence.py`: the UX Evidence Graph query/evaluate engine, used for product-fit scoring
  of candidate sources against a context vector.
- `ii/mcp.py`: read-only-by-default MCP tool registration pattern; source read tools follow it.
- `ii/atlas.py`, `ii/studio.py`: static catalogue generation and a read-only local viewer.
- `ii/repair.py`, `ii/apprunner.py`, `ii/browser.py`: isolated git worktree, safe process
  runner, real browser capture; reused by the adaptation/implementation path (experimental).
- `make check` + secret scan: the deterministic offline gate.

## Implemented before this version (relevant)
- Evidence-grounded audit and the colour-only-status repair (Vue), browser-verified in CI.
- The capability matrix and the honesty discipline (implemented / experimental / unsupported).

## Status of the source-intelligence capability before this version
- **Missing:** any third-party source registry, discovery, assurance, quarantine, contribution,
  or source CLI/MCP. There is a `ux-evidence/schemas/source.schema.json`, but that describes
  evidence *citations*, not reusable UI libraries; it is unrelated and untouched.

## Plan classification for this build
- **Implemented (this release):** registry schema and structure; a deduplicated seed list
  across all categories as `seed-unreviewed` (names and candidate URLs only, everything else
  unverified); offline local search, compare, recommend; deterministic Source Assurance checks;
  reuse-mode classification; adaptation-plan generation; quarantine; contribution-bundle
  generation with privacy stripping; GitHub PR preparation; a generated README catalogue;
  source CLI and read-only MCP tools; a CI validation workflow; tests; the command-palette
  vertical slice (query -> compare -> verify -> recommend -> adapt-plan).
- **Experimental:** live web/GitHub/npm/Storybook discovery providers (offline fixtures and
  explicit opt-in only); automated primary-source verification; component-level browser testing
  of candidates; PR automation; implementation-agent handoff for real component installation.
- **Unsafe / never:** silent crawling; network activity during install/audit/repair/CI;
  automatic central-registry writes; automatic trust upgrades; unrestricted installation;
  licence/security/accessibility certification; copying paid or proprietary source code.

## Honesty constraints adopted
- Seed sources are **not** trusted. Verified fields stay `unknown`/`unverified` with
  `confidence: 0.0` and `verified_from_primary_source: false` until evidence is recorded. No
  marketing claim is copied into a verified field.
- Discovery is **disabled by default**, opt-in, explicit, rate-limited, cached, robots-aware,
  local-first, and cannot upload private project data or auto-merge contributions.
- All discovered web content is treated as hostile, inert data (prompt-injection defence).

## Regression risk
- New `source-registry/` data and `ii/sources.py` are additive; existing engines and the
  v3.0.0 release are untouched. `make check` continues to gate offline.
