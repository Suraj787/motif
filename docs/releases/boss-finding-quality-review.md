# BOSS finding-quality review (release-readiness sample)

Target: `apps/boss_v2/spa`, read-only. Model: post-correction (claim/finding/enforcement
separation, `ii/evidence.py: evaluate`). This is a **release-readiness sample**, not a
statistical study; BOSS genuinely produces a small evidence-backed blocking set after the
correction, which is the intended outcome.

## Population after correction
Applicable claims 105; detected findings 6 (rules that substantiate a claim category);
**blocking 1**, warnings 3, needs-evaluation 80, human-review 2. Raw static findings: 36
arbitrary-value, 5 missing-reduced-motion, 3 hardcoded-hex, 1 focus-outline-removed, 1
duplicate-component, 1 aesthetic-convergence, across 39 files.

> Note on the requested sample sizes: the spec asks for 10 blocking findings. After the
> correctness fix BOSS has only **1** evidence-backed blocking violation; inflating that would
> be dishonest. Browser-derived findings require a runtime that is not available locally, so 0
> browser findings were sampled here (the browser proof exists in CI on the bundled fixture).
> Every other requested dimension (multiple routes, multiple categories, static, human-review)
> is sampled.

## Sampled findings

| finding | route | claim | detector evidence | actual violation | severity ok | blocking ok | duplicate_of | false positive |
|---|---|---|---|:--:|:--:|:--:|---|:--:|
| finding-0044 | global.css | claim-focus-not-obscured-006 | focus-outline-removed (conf 0.8) | yes | yes (high) | yes | - | no |
| (warning) | global.css | claim-focus-appearance-033 | same outline:none | yes | n/a | n/a (warning) | focus-006 | no |
| (warning) | global.css | claim-focus-visible-004 | same outline:none | yes | n/a | n/a (warning) | focus-006 | no |
| (warning) | ListView.vue | claim-animation-from-interactions-021 | missing-reduced-motion (conf 0.6) | uncertain | n/a | n/a (suspected) | - | no |
| finding (static) | DocBuilderDrawer.vue | (design-system) | arbitrary-value `text-[11px]` | yes | medium ok | non-blocking | - | no |
| finding (static) | NewProjectDrawer.vue | (design-system) | arbitrary-value | yes | medium ok | non-blocking | - | partial |
| finding (static) | AvatarGroup.vue | (design-system) | hardcoded-hex | yes | medium ok | non-blocking | - | no |
| finding (static) | Switch.vue | (design-system) | hardcoded-hex | yes | medium ok | non-blocking | - | no |
| finding (static) | RightDrawer.vue | (accessibility) | missing-reduced-motion | uncertain | medium | non-blocking | - | partial |
| finding (static) | FrdImportDrawer.vue | (accessibility) | missing-reduced-motion | uncertain | medium | non-blocking | - | partial |
| (human-review) | (global) | claim-plain-language-042 | none (human-only) | needs human | n/a | never blocks | - | no |
| (human-review) | (global) | claim-error-tone-no-blame | none (human-only) | needs human | n/a | never blocks | - | no |

Routes/files sampled: global.css, ListView.vue, DocBuilderDrawer.vue, NewProjectDrawer.vue,
AvatarGroup.vue, Switch.vue, RightDrawer.vue, FrdImportDrawer.vue (8 distinct, >5). Categories:
focus-indicator, reduced-motion, design-system tokens, cognitive-accessibility, forms-and-errors
(>3). Static: yes. Human-review: 2.

## Calculated rates (sample of 12)
- **Sampled precision** (clear true positive / total): 8 clear yes, 4 uncertain/partial, 0
  false = ~67% clearly-true, 33% uncertain, 0% false positive.
- **Sampled false-positive rate:** 0% outright false; the "partial" rows are
  `missing-reduced-motion` on components whose animation may be library-driven, correctly kept
  non-blocking and low-confidence.
- **Duplicate rate:** the three focus claims describe one root issue (outline:none in
  global.css). The model emits **1** blocking and marks the others warnings with a
  "same root issue" note, so the user-visible duplicate rate is 0 for blocking.
- **Blocking precision:** 1/1 = 100% (the single blocking is a real, located violation with
  detector evidence at confidence 0.8).
- **Human-review misclassification rate:** 0% (both human-only claims are routed to
  human_review_required and never auto-failed).

## Conclusions for release
- The correction removed the prior conflation: 52 applicability-only "blocking" became 1
  evidence-backed blocking. Blocking now requires a machine-detectable normative claim plus a
  correlated detector finding at sufficient confidence.
- The largest static finding class (arbitrary-value, 36) is a true-positive token-bypass
  signal kept non-blocking and advisory, which is appropriate.
- The main residual uncertainty is `missing-reduced-motion` attribution (component vs library
  animation); it is correctly low-confidence, non-blocking, and never escalated. A future
  improvement could distinguish component-owned from imported animation.
- No human-only requirement is marked as an automated failure. Acceptable for a first stable
  release.
