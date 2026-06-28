# Source Intelligence vertical slice

Demonstration (§29): an accessible command palette for an enterprise React application used
daily by keyboard-heavy users. Run offline against the seed registry; nothing is trusted
automatically and no network is used.

## Walkthrough (real CLI output)

### 1. Search framework-appropriate candidates
```
motif sources search "" --framework react
  -> ariakit, base-ui, headless-ui, radix-ui, react-aria, shadcn-ui, ...
```
Interaction-correct foundations rank above decorative libraries for an accessible,
keyboard-heavy need.

### 2. Compare two candidates
```
motif sources compare radix-ui ariakit
  radix-ui  reuse_mode=pattern-extraction  licence_verified=false
  ariakit   reuse_mode=pattern-extraction  licence_verified=false
```
Both rows reflect recorded evidence only; unverified licence is an honest gap, not a guess.

### 3. Verify (deterministic assurance)
```
motif sources verify radix-ui
  decision: insufficient-evidence
  blocked_modes: [direct-reuse]
  allowed_modes: [inspect, pattern-extraction]
  approval_required: true
```
No primary-source licence/identity/security/accessibility evidence is recorded, so direct
reuse is blocked. Study and pattern extraction remain allowed.

### 4. Recommend a strategy
```
motif sources recommend --need "command palette" --product-form enterprise-app \
  --workflow daily-operation --framework react --ability keyboard-only
  recommended_strategy: pattern-extraction-or-internal-implementation
  rationale: No source has verified licence + identity + security + accessibility, so no
             direct reuse is justified. Recommend pattern extraction or an internal,
             evidence-grounded implementation.
```
The recommendation ranks by recorded evidence, not visual impressiveness. With 55 applicable
normative requirements for this context, the safest path is to extract the interaction model
(keyboard navigation, focus trap, ARIA combobox/listbox) and implement it internally.

### 5. Adaptation plan (handed to the implementation agent, not raw approval)
```
motif sources adapt-plan radix-ui --target ./app
  reuse_mode: pattern-extraction
  accessibility_repairs: [verify keyboard operability, ensure visible focus,
                          do not rely on colour alone, check target size]
  motion_policy: [respect prefers-reduced-motion]
  security_constraints: [remove telemetry, no remote code loading, sanitise any HTML]
  rollback: apply in an isolated git worktree; exact rollback if rejected
```

## What this proves
- Motif can query, compare, verify, recommend, and produce an adaptation plan for a real need
  entirely offline, without trusting any seed source.
- It does not select the most visually impressive option; it ranks by evidence and, when no
  verified source exists, recommends pattern extraction or internal implementation.

## Honest limits of the slice
- Steps 7-10 of the full vision (implement in a worktree, run component-level browser
  assurance, report compromises, roll back) reuse the existing isolated-worktree and browser
  machinery and remain **experimental** for arbitrary third-party components: no seed source is
  verified, so no direct installation is performed.
- The second demonstration (comparing animated marketing-section libraries) is supported by the
  same compare/verify commands, but every such source is `seed-unreviewed`, so the output is a
  structured "insufficient evidence; study only" result rather than a reuse decision.
