# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Deepen per-source component catalogues with previews and more verified records.
- Implement live network connectors for the source-refresh workflow (currently declarative).
- Grow recipe and adapter coverage (Angular, more Svelte/vanilla).
- Re-verify `pending-verification` and medium-confidence licences on a schedule.

## [1.0.0] - 2026-06-27

Broadens coverage to a thoroughly reviewed source set with web-verified licences, expands
the catalogues, and matures the controlled installer. The architecture, security model and
honesty discipline from 0.1.0 are unchanged.

### Added

- **Source set expanded 22 → 90.** Every new source's licence was verified against its
  actual `LICENSE` file, `package.json` `license` field, or official terms page (recorded
  under `evidence`). Split: 53 redistributable, 20 adaptable-concept, 17 reference-only.
- **Component catalogue expanded 10 → 64**, across all five usability modes (37 installable,
  17 adaptable, 9 reference-only, 1 rejected).
- **Taxonomies expanded**: effects 14 → 30, patterns 16 → 28; recipes 4 → 14 with real,
  dependency-free, reduced-motion-aware clean-room implementations across browser-native,
  Vue, Frappe-Vue, React and Svelte.
- **Matured controlled installer.** New `motif/project.py` detects the target's framework,
  TypeScript/Tailwind and installed dependencies; the install plan now includes a
  framework-compatibility gate, a dependency plan against the project's `package.json`, and
  a static security scan of the implementation before applying.
- **`THIRD_PARTY_SOURCES.md` regenerated from the registry** so it always matches the
  records, with a section documenting notable licence nuances.

### Changed

- `make check` now runs 60 self-checks (added project detection, dependency planning and
  the larger registry).
- Documentation, README and the research methodology updated with the verification pass and
  corrected licence facts (p5.js LGPL, ScrollReveal GPL-3.0, Shopify Polaris field-of-use,
  vue-bits/svelte-bits Commons Clause, Theatre.js dual-licensed, Salesforce SLDS split).

### Notes

Live network connectors remain declarative (specified, not yet implemented); the
source-refresh workflow is offline in this release. Licence facts are confidence-rated;
re-verify before bundling anything new.

## [0.1.0] - 2026-06-27

Initial release. Ships the **complete architecture and secure pipeline** with
**representative, high-confidence breadth** rather than fabricated volume.

### Added

- **Interaction-design intelligence model.** The 8-level reasoning model
  (development purpose → product type → user intent → page/screen type → interaction
  objective → pattern → effect → implementation), taxonomies, anti-patterns and 10 quality
  profiles in `intelligence/`. Distinguishes **websites** from **web applications** and
  searches PATTERNS before EFFECTS.
- **Orchestrator skill + specialists.** A root `SKILL.md` that loads knowledge
  selectively, 10 specialist skills in `skills/`, 8 reviewer agents and reusable runbooks
  in `workflows/`.
- **Secure ingestion pipeline.** Offline approved registry as the default runtime; explicit
  `source retrieve --refresh` against an allowlisted official host; untrusted-by-default
  quarantine (`.motif/quarantine|reviewed|approved|rejected/`) where retrieved code is never
  executed. Security policies in `security/*.yml`.
- **Five static scanners** in `scanners/`: `source_scanner`, `behaviour_scanner`,
  `dependency_scanner`, `license_scanner`, `secret_scanner`.
- **Licence & source governance.** The LICENCE GATE (unknown ⇒ reference-only),
  trust tiers 1-5, redistribution classes, `registry/licenses/`, `LICENSE_POLICY.md` and
  `THIRD_PARTY_SOURCES.md`. Original code is MIT-licensed.
- **Representative registry.** 22 reviewed sources (licence/redistribution classified, a
  few `pending-verification`), 10 component records spanning all five usability modes
  (including a rejected fixture), 14 effects, 16 patterns, 4 clean-room recipe
  implementations and 10 quality profiles.
- **CLI and transparent ranking.** A dependency-free `python -m motif` CLI (Python 3.11+,
  stdlib only) with registry search, transparent candidate ranking, controlled install
  (plan → snapshot → patch → validate → auto-rollback → provenance manifest), validation
  and a health `doctor`.
- **Framework adapters & clean-room implementations.** Adapter contract plus
  browser-native, Vue, Frappe-Vue and React implementations in `adapters/` and
  `implementations/`.
- **Evaluations.** 12 evaluation cases (judgement + security) and malicious fixtures in
  `evals/`.
- **Schemas.** 7 strict JSON Schemas in `schemas/` (source, component, effect, pattern,
  recipe, decision, evaluation) that every record must satisfy.
- **CI and local gate.** `make check` (runs `motif validate`, `tools/selfcheck.py` and the
  secret scan) mirrored by `.github/workflows/ci.yml`.
- **Open-source readiness.** README, `CONTRIBUTING.md`, `SECURITY.md`,
  `CODE_OF_CONDUCT.md`, this changelog, issue/PR templates and a pre-release self-review.

### Notes

This is representative breadth, not full coverage. Licence facts are confidence-rated and
**must be re-verified online** before any material is bundled; some sources remain
`pending-verification`. Live network connectors are specified but not implemented in this
release.

[Unreleased]: https://github.com/Suraj787/motif/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Suraj787/motif/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/Suraj787/motif/releases/tag/v0.1.0
