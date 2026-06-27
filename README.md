# Open Interaction Intelligence (OII)

**Interaction-design intelligence and governance for AI coding agents** — securely
discover, select, adapt and validate UI motion, effects and interaction patterns
for websites and web applications.

> This is **not** an animation bundle, a list of effect websites, or a prompt that
> sprinkles random motion. It is a reasoning + governance system. Its first job is
> to decide what the user needs to *understand, feel or accomplish*, then choose the
> **least complex interaction** that achieves it — and to refuse motion that hurts
> usability, accessibility, performance or licensing.

[![CI](https://github.com/Suraj787/open-interaction-intelligence/actions/workflows/ci.yml/badge.svg)](https://github.com/Suraj787/open-interaction-intelligence/actions)
&nbsp;Licence: MIT · Status: v0.1.0

---

## What it does

OII reasons from product context down to implementation, **searching for a pattern
before an effect**:

```
development purpose → product type → user intent → page/screen type
→ interaction objective → pattern → effect → implementation
```

It distinguishes **websites** from **web applications**, keeps **Vue and Frappe-Vue
first-class** alongside React and browser-native, and treats **accessibility +
reduced-motion as mandatory**, never optional.

## Why it's safe

The tempting-but-dangerous path — scrape a site, run its install script, copy its
code into your project — is the *hard* path here. Instead:

- **Offline approved registry is the default.** Normal use reads the committed local
  registry and never touches the network. Internet retrieval happens only through an
  explicit `source retrieve --refresh` against an allowlisted official host.
- **Untrusted-by-default ingestion.** Retrieved material lands in `.oii/quarantine/`
  and is **never executed**. Five static scanners (dangerous patterns, browser
  behaviour, dependencies, licence, secrets) review it before anything is approved.
- **Licence gate.** Unknown licence ⇒ `reference-only`, never bundled. Source-available
  / Commons-Clause terms are not treated as permissive OSS.
- **Controlled installation.** Plan → snapshot → controlled patch → validate →
  auto-rollback on failure → provenance manifest. Third-party installers are never run
  against your project.

> OII reduces risk but **cannot guarantee** third-party code is completely safe. Human
> review remains required. See [`docs/threat-model.md`](docs/threat-model.md).

## Quick start

```bash
# no dependencies required for the core CLI (stdlib only, Python 3.11+)
python -m oii doctor              # environment + registry health
python -m oii validate            # validate the registry against schemas
python -m oii search "save"       # search patterns/effects/recipes
python -m oii rank skeleton-loading --profile enterprise-strict   # transparent ranking
python -m oii source completeness # component coverage by source
python -m oii source scan evals/fixtures/eval-button   # run the scanners on a path
make check                        # the full local gate (mirrors CI)
```

### Use with Claude Code / Agent Skills

The root [`SKILL.md`](SKILL.md) is an **orchestrator** (not a knowledge dump): it
inspects your repo, classifies the product/page/user/problem, loads only the relevant
local intelligence, produces and **transparently ranks** candidates, selects the
simplest effective approach in your framework, then validates accessibility,
performance and responsiveness before recording the decision and provenance.
Specialist skills live in [`skills/`](skills/); reusable runbooks in
[`workflows/`](workflows/).

## Repository map

| Area | What's there |
|------|--------------|
| `SKILL.md`, `skills/`, `agents/` | Root orchestrator + 10 specialist skills + 8 reviewer agents |
| `intelligence/` | The 8-level model, taxonomies, anti-patterns, 10 quality profiles |
| `registry/` | Machine-readable sources, components, effects, patterns, recipes, licences |
| `schemas/` | 7 strict JSON Schemas every record must satisfy |
| `connectors/`, `ingestion/`, `security/`, `scanners/` | Secure retrieval pipeline + policies + 5 scanners |
| `adapters/`, `implementations/` | Framework contracts + clean-room implementations (browser-native, Vue, Frappe-Vue, React) |
| `oii/` | The dependency-free Python CLI (search, ranking, install, validation) |
| `evals/` | Judgement + security evaluations and malicious fixtures |
| `examples/` | Worked decision records (enterprise dashboard, ERP form, SaaS hero, …) |
| `docs/` | Architecture, threat model, authoring guides, ADRs |

## What v0.1.0 honestly contains

Per the project's release discipline, v0.1.0 ships the **complete architecture and
secure pipeline** with **representative, high-confidence breadth** rather than
fabricated volume:

- 22 reviewed sources (licence/redistribution classified; a few `pending-verification`)
- 10 component records spanning all five usability modes (incl. a rejected fixture)
- 14 effects · 16 patterns · 4 clean-room recipe implementations · 10 quality profiles
- Working search, transparent ranking, controlled install + rollback, 5 scanners
- 12 evaluation cases (judgement + security) and a dependency-free `make check`

Licence facts are marked with a confidence level and **must be re-verified online**
through the source-refresh workflow before bundling. See
[`THIRD_PARTY_SOURCES.md`](THIRD_PARTY_SOURCES.md) and
[`docs/research-methodology.md`](docs/research-methodology.md).

## Roadmap

- **v0.2.0** — broaden to 40–50 sources, expand component coverage, strengthen installer
  automation, add more tested recipes.
- **v1.0.0** — 75–100 thoroughly reviewed sources, broad component coverage, mature
  adapters, a proven contributor workflow.

## Contributing & security

See [`CONTRIBUTING.md`](CONTRIBUTING.md), [`SECURITY.md`](SECURITY.md) and
[`LICENSE_POLICY.md`](LICENSE_POLICY.md). AI-generated contributions require human
review. The strongest version of this project is not the one with the most effects —
it is the one that selects the right effect, proves where it came from, adapts it
safely, and refuses inappropriate motion.

## Licence

Original OII code is [MIT](LICENSE). This licence covers only original code; every
third-party source keeps its own licence and obligations.
