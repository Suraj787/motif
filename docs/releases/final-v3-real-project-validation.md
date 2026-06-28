# Final v3 real-project validation

Audit-only, read-only validation across three real projects beyond the bundled Vue fixture.
None were modified; no `.motif` state was written into any of them. Post-correction model
(claim/finding/enforcement separation).

| Metric | BOSS (Vue) | React (digital_concierge) | AI-generated (vite_react_shadcn_ts) |
|---|---:|---:|---:|
| Project detected | frappe-vue | react | react |
| Package manager | npm | yarn | npm |
| App started | not-executed (1) | not-executed (1) | not-executed (1) |
| Routes audited | 14 | 0 (2) | 0 (2) |
| Browser capture completed | not-executed (1) | not-executed (1) | not-executed (1) |
| Axe completed | not-executed (1) | not-executed (1) | not-executed (1) |
| Applicable claims | 105 | 105 | 110 |
| Actual findings (static) | 47 | 25 | 99 |
| Blocking findings (evidence-backed) | 1 | 1 | 2 |
| Human-review findings | 2 | 2 | 2 |
| Sampled false positives | 0 outright | 0 outright | 0 outright |
| Originality score | 19 | 15 | 41 |
| Originality confidence | low | low | moderate |
| Cleanup successful | yes | yes | yes |
| Source files modified | 0 | 0 | 0 |

(1) Browser stages require the optional browser runtime, which is not available in this local
environment; they are honestly reported `not-executed` and never faked. The browser proof of
the golden loop exists in CI on the bundled Vue fixture (real Chromium).

(2) Route count is 0 for the React projects because route discovery currently parses
vue-router conventions; react-router is not yet parsed. Documented framework assumption.

## What this shows
- **Framework generality:** detection works on Vue and React, with correct per-project
  package-manager detection (npm vs yarn). Vue-specific assumptions are not applied to the
  static finding and evidence layers.
- **Evidence-backed blocking:** each project yields a small, evidence-backed blocking set
  (1-2), never the applicability-only inflation the correction removed. Blocking on all three
  is a focus-indicator violation with `focus-outline-removed` evidence at confidence 0.8.
- **Originality discrimination without authorship claims:** the AI-generated app scores 41
  (moderate) versus 15-19 (low) for the hand-built apps, driven by explainable decorative
  signals (`gradient-hero`, `glass-blur`) and a very high `excessive-rounded` raw count (162)
  that is correctly down-weighted. The detector reports aesthetic-convergence risk and does
  not claim the UI was produced by AI.

## Unsupported capabilities (failed safely / not attempted)
- Repair: only the colour-only-status class on Vue is implemented. No repair was attempted on
  any project; unsupported repair paths are not invoked in audit-only mode.
- Browser capture / app startup / axe: require the runtime; reported not-executed.
- Authenticated flows and multi-route crawling: not attempted.

## Framework assumptions and detector limitations
- react-router route discovery is not implemented (routes report 0 for React).
- `missing-reduced-motion` attribution can over-report when animation is library-owned; kept
  low-confidence and non-blocking.
- Originality is static and capped at moderate confidence.

## Report usability, cleanup, and rollback
- Each audit emits a structured result with detection, evaluate (claim/finding/enforcement
  separation), and an originality signal breakdown. Output is inspectable and reproducible.
- Cleanup: no `.motif` directory was created in any target; 0 source files modified. The
  golden repair loop (the only mutating path) operates exclusively in an isolated worktree and
  was not invoked here.
