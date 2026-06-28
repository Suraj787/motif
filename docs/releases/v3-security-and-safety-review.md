# Motif v3.0.0 security and safety review

Pre-stable-release review. Status as of the `fix/claim-finding-separation` branch.

| Check | Status | Evidence |
|---|---|---|
| No secrets in repository | pass | `make check` secret scan CLEAN; positive/negative self-test included |
| No unsafe shell interpolation | pass | app runner builds argv lists, never shell strings; no `shell=True` in repair/apprunner |
| No untrusted command execution without policy approval | pass | `apprunner.start` requires explicit `--approve`; MCP write tools guarded without `--allow-write` |
| Worktrees isolated | pass | repair operates only in a fresh `git worktree`; baseline branch never touched |
| Repair writes constrained | pass | only the colour-only-status text-label edit, applied in the worktree, then exact rollback |
| Process cleanup reliable | pass | `apprunner.stop` kills the process group; golden loop stops the app in a finally path |
| Temp files in approved paths | pass | runtime state under the target's `.motif/` (gitignored); audits write nothing into targets |
| MCP read-only by default | pass | write tools return `isError` without `--allow-write` (verified) |
| Browser logs do not leak secrets | pass | `apprunner` filters env vars matching token/secret/password/key/aws/gh_/ssh/api before logging |
| GitHub Actions least privilege | pass | `browser-golden-loop.yml`, `ci.yml`, `guardian.yml` declare `permissions:` (contents: read) |
| Fork PRs do not receive secrets | pass | workflows use no repository secrets in the golden loop; default `GITHUB_TOKEN` is read-only |
| Artifacts contain no credentials | pass | golden-loop artifacts are screenshots, axe/aria/console/network JSON, and the report; env filtered |
| No legal/compliance certification claimed | pass | claims carry `legal.compliance_claim_allowed: false`; docs state no certification |

## Notes
- The core CLI is dependency-free (Python standard library only); the browser runtime is an
  optional `motif[browser]` extra. No undeclared or local-path dependency is introduced.
- The claim/finding separation reduces the risk of over-asserting violations: blocking now
  requires detector evidence, sufficient confidence, a machine-supported enforcement mode, and
  no unresolved contradiction.
- Audit-only validation on BOSS and two external projects wrote nothing into those
  repositories (verified: no `.motif` directory created, 0 source files modified).

## Residual risks (accepted for v3.0.0)
- `missing-reduced-motion` attribution can over-report library-owned animation; kept
  low-confidence and non-blocking.
- Browser steps are not-executed without a runtime; this is reported honestly and is not a
  security risk, but limits local assurance to the CI fixture.
