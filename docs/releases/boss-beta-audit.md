# Motif v3.0.0-beta.1 audit-only validation against BOSS v2 SPA

Date: 2026-06-28. Mode: **audit-only, read-only**. Target: `apps/boss_v2/spa` (real Vue 3 +
Vite + frappe-ui SPA). No repair was applied; nothing was written into the BOSS tree
(verified: `git status` in BOSS shows zero Motif artifacts after the run).

## Project detection (correct)
frappe-vue, TypeScript, Tailwind; 14 routes, 59 components, 27 dependencies; start `npm run
dev`, build `npm run build`. Motif correctly identified the Frappe-Vue framework from
`frappe-ui` rather than mislabelling it plain Vue.

## Findings (static)
47 findings: 39 design-system, 6 accessibility, 1 duplication, 1 originality. Severity: 46
medium, 1 high. Debt score 54/100 (moderate) over 99 files; categories: arbitrary-value,
hex-colour-inline, important, inline-style, missing-reduced-motion, todo-fixme.

## False-positive review (sampled)
| Class | Verdict | Notes |
|---|---|---|
| `arbitrary-value` (e.g. `text-[11px]`, `w-[..]`) | **true positive** | Genuinely bypasses the type/space scale; legitimate debt signal. A minority are acceptable one-offs, so treat as advisory, not blocking. |
| `hardcoded-hex` | mostly true | Real hex literals; some are brand colours in a theme file that should be tokenised once, not per-occurrence. |
| `missing-reduced-motion` | needs-context | Fires per component containing animation without a `prefers-reduced-motion` guard. Some are driven by library components (driver.js, canvas-confetti); attribution to the component file can over-report. |
| `duplication` (1) | plausible | Near-duplicate drawer/modal naming; worth a human look. |
| `originality` convergence = 100 | **false positive** | See below. |

## Two real Motif weaknesses surfaced (fix before stable v3.0.0)

### 1. Aesthetic Convergence Detector saturates on enterprise UI (false positive, high)
Convergence scored 100/100 on BOSS. The firing signals were `excessive-rounded` (48),
`three-feature-cards` (22), `pill-overuse` (13), `gradient-hero` (9), `glass-blur` (7).
`rounded-*`, status pills, and `card` containers are normal, appropriate enterprise Tailwind
UI, not the "generic AI hero" cliche the detector targets. The regexes are context-blind and
count common utility classes. **Recommendation:** make the detector context-aware (skip
`three-feature-cards`/`excessive-rounded`/`pill-overuse` for enterprise/dashboard profiles),
weight by density rather than raw count, and cap any single signal's contribution.

### 2. Evidence query over-filters rich contexts (high)
A minimal context (abilities only) returned 16 applicable claims; the realistic 8-dimension
BOSS context returned **0**. Root cause: all 110 claims fill **every** applicability
dimension (110/110 specify `product_forms`, `purposes`, `workflows`, `devices`...), and the
engine excludes a claim if any dimension it specifies fails to overlap the context. A
detailed context therefore matches almost nothing. **Recommendation:** either author claims
to leave a dimension empty unless the claim is genuinely specific to it, or change the merge
to rank by specificity (partial-match scoring) instead of hard-excluding on every specified
dimension. This is the most important correctness fix before stable.

## Context assumptions
The BOSS context vector marked `risks`, `abilities`, and `environments` as assumptions (no
project documentation or interviews were used). The engine correctly returned overall
confidence `low`. This honesty behaviour worked as intended.

## Browser reliability
`doctor --browser`: not available in this environment (`pip` broken locally). All
browser-executed audit steps are therefore `not-executed` here. The browser proof of the
golden loop exists only in CI, and only against the bundled Vue fixture, not BOSS.

## Report quality
- Strengths: findings are typed, located (file + line), and severity-rated; debt has a
  category breakdown; the evidence query exposes confidence and conflicts; nothing claimed
  full accessibility or certification.
- Gaps: the originality CLI output shows only an aggregate score, not the per-signal
  breakdown that reveals the false positives (the breakdown exists in the module but is not
  surfaced); a 0-applicable evidence result gives no explanation of why nothing matched.

## Verdict for the beta
The deterministic detectors run cleanly on a real, non-fixture project and produce
explainable, located findings without modifying it. Two real defects (originality
saturation, evidence over-filtering) and a reporting gap should be fixed before a stable
v3.0.0. The colour-only browser repair is proven only on the bundled fixture and was
correctly not attempted on BOSS.

## Reproduce (read-only)
A read-only audit script (project model, findings, debt, originality, design-system extract,
evidence query, state inspection, `doctor --browser`) was run against BOSS; it writes nothing
into the target. See the validation plan in `beta-validation-plan.md`.
