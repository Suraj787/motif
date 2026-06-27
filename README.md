# Motif

**Interaction-design intelligence and governance for AI coding agents.** Motif helps
agents securely discover, select, adapt and validate UI motion, effects and
interaction patterns for websites and web applications.

> This is not an animation bundle, a list of effect websites, or a prompt that
> sprinkles random motion. It is a reasoning and governance system. Its first job is
> to decide what the user needs to understand, feel or accomplish, then choose the
> **least complex interaction** that achieves it, and to refuse motion that hurts
> usability, accessibility, performance or licensing.

[![CI](https://github.com/Suraj787/motif/actions/workflows/ci.yml/badge.svg)](https://github.com/Suraj787/motif/actions)
&nbsp;Licence: MIT. Status: v1.0.0

---

## What it does

Motif reasons from product context down to implementation, and it searches for a
pattern before an effect:

```
development purpose > product type > user intent > page/screen type
> interaction objective > pattern > effect > implementation
```

It distinguishes websites from web applications, keeps Vue and Frappe-Vue first-class
alongside React and browser-native, and treats accessibility and reduced-motion as
mandatory rather than optional.

## Why it's safe

The tempting-but-dangerous path (scrape a site, run its install script, copy its code
into your project) is the hard path here. Instead:

- **Offline approved registry is the default.** Normal use reads the committed local
  registry and never touches the network. Internet retrieval happens only through an
  explicit `source retrieve --refresh` against an allowlisted official host.
- **Untrusted-by-default ingestion.** Retrieved material lands in `.motif/quarantine/`
  and is never executed. Five static scanners (dangerous patterns, browser behaviour,
  dependencies, licence, secrets) review it before anything is approved.
- **Licence gate.** Unknown licence becomes `reference-only`, never bundled.
  Source-available and Commons-Clause terms are not treated as permissive OSS.
- **Controlled installation.** Plan, snapshot, controlled patch, validate, auto-rollback
  on failure, then a provenance manifest. Third-party installers never run against your
  project.

> Motif reduces risk but cannot guarantee that third-party code is completely safe.
> Human review remains required. See [`docs/threat-model.md`](docs/threat-model.md).

## Installation

**Requirements:** Python 3.11+ and `git`. Node.js 18+ is optional (only for
adapter/implementation tooling). The core CLI has no Python dependencies, so it runs on
a stock interpreter.

### 1. Get the repository

```bash
git clone https://github.com/Suraj787/motif.git
cd motif
```

### 2. Use it (pick one)

**Option A, run in place with zero install.** From the repo root:

```bash
python -m motif doctor      # checks environment and registry
make check                  # full local gate (validation, scanners, ranking)
```

**Option B, install the `motif` command.** This adds an entry point so you can call
`motif` from anywhere. Add `[dev]` for the pytest and ruff toolchain used by CI:

```bash
python -m pip install -e .          # gives the `motif` command
python -m pip install -e ".[dev]"   # plus pytest, ruff (optional)
motif doctor
```

### 3. Use it as a Claude Code Agent Skill

Point Claude Code at this repo (open it as your working directory, or copy/symlink the
skill folders into your skills path). The root [`SKILL.md`](SKILL.md) is the
orchestrator; specialist skills live in [`skills/`](skills/). For example:

```bash
# expose the skills to a Claude Code skills directory (adjust the target path)
ln -s "$(pwd)/skills" ~/.claude/skills/motif-specialists
ln -s "$(pwd)/SKILL.md" ~/.claude/skills/motif.md
```

Then verify with `python -m motif validate` (it should report `OK`).

## Quick start

```bash
# no dependencies required for the core CLI (stdlib only, Python 3.11+)
python -m motif doctor              # environment and registry health
python -m motif validate            # validate the registry against schemas
python -m motif search "save"       # search patterns/effects/recipes
python -m motif rank skeleton-loading --profile enterprise-strict   # transparent ranking
python -m motif source completeness # component coverage by source
python -m motif source scan evals/fixtures/eval-button   # run the scanners on a path
make check                          # the full local gate (mirrors CI)
```

### Use with Claude Code / Agent Skills

The root [`SKILL.md`](SKILL.md) is an orchestrator, not a knowledge dump. It inspects
your repo, classifies the product/page/user/problem, loads only the relevant local
intelligence, produces and transparently ranks candidates, selects the simplest
effective approach in your framework, then validates accessibility, performance and
responsiveness before recording the decision and provenance. Specialist skills live in
[`skills/`](skills/); reusable runbooks in [`workflows/`](workflows/).

## Repository map

| Area | What's there |
|------|--------------|
| `SKILL.md`, `skills/`, `agents/` | Root orchestrator, 10 specialist skills, 8 reviewer agents |
| `intelligence/` | The 8-level model, taxonomies, anti-patterns, 10 quality profiles |
| `registry/` | Machine-readable sources, components, effects, patterns, recipes, licences |
| `schemas/` | 7 strict JSON Schemas every record must satisfy |
| `connectors/`, `ingestion/`, `security/`, `scanners/` | Secure retrieval pipeline, policies, 5 scanners |
| `adapters/`, `implementations/` | Framework contracts and clean-room implementations (browser-native, Vue, Frappe-Vue, React) |
| `motif/` | The dependency-free Python CLI (search, ranking, install, validation) |
| `evals/` | Judgement and security evaluations, plus malicious fixtures |
| `examples/` | Worked decision records (enterprise dashboard, ERP form, SaaS hero, and more) |
| `docs/` | Architecture, threat model, authoring guides, ADRs |

## What v1.0.0 contains

v1.0.0 broadens coverage to a thoroughly reviewed source set while keeping every record
honest:

- **90 reviewed sources**, each new one's licence verified against its actual `LICENSE`
  file, `package.json`, or official terms page (recorded under `evidence`). Split: 53
  redistributable, 20 adaptable-concept, 17 reference-only.
- **64 component records** across all five usability modes (37 installable, 17 adaptable,
  9 reference-only, 1 rejected), each carrying the source's licence and a usability mode.
- **30 effects, 28 patterns, 14 clean-room recipe implementations**, 10 quality profiles.
- Working search, transparent ranking, and a controlled installer with framework
  detection, dependency planning, a static security scan, snapshot and rollback.
- 5 scanners, malicious fixtures, 12+ evaluation cases, and a dependency-free `make check`
  (60 self-checks).

Licence facts carry a confidence level. The verification pass corrected several naive
assumptions (p5.js is LGPL, ScrollReveal is GPL-3.0, Shopify Polaris is field-of-use
restricted, vue-bits/svelte-bits carry a Commons Clause, Theatre.js is dual-licensed).
See [`THIRD_PARTY_SOURCES.md`](THIRD_PARTY_SOURCES.md) and
[`docs/research-methodology.md`](docs/research-methodology.md).

## Roadmap beyond v1.0.0

- Deepen component catalogues per source (more verified records, previews).
- Implement live network connectors for the source-refresh workflow (currently declarative).
- Grow the recipe library and adapter coverage (Angular, more Svelte/vanilla).
- Re-verify `pending-verification` and medium-confidence licences on a schedule.

## Contributing and security

See [`CONTRIBUTING.md`](CONTRIBUTING.md), [`SECURITY.md`](SECURITY.md) and
[`LICENSE_POLICY.md`](LICENSE_POLICY.md). AI-generated contributions require human
review. The strongest version of this project is not the one with the most effects. It
is the one that selects the right effect, proves where it came from, adapts it safely,
and refuses inappropriate motion.

## Licence

Original Motif code is [MIT](LICENSE). This licence covers only original code; every
third-party source keeps its own licence and obligations.
