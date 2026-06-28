# ADR-SRC-001: Federated source discovery and contribution

Status: accepted. Date: 2026-06-28. Version: v3.1.0.

## Context
Motif needs to help both improve existing UIs and build new ones by drawing on the public
ecosystem of component libraries, design systems, templates, and inspiration. Doing this
naively (crawl the web on every run, trust what is found, write it into a central registry)
would be unsafe: it would leak private project data, execute or trust hostile content, and
let a single installed copy poison a shared registry.

## Decision
Adopt a federated, offline-first architecture with explicit human gates:

```
Offline trusted registry snapshot
  -> optional explicit discovery (opt-in, rate-limited, cached, robots-aware)
  -> local quarantine
  -> deterministic Source Assurance
  -> user review
  -> optional contribution bundle or pull request
  -> central CI verification
  -> human maintainer approval
  -> signed registry update
```

### Why Motif does not crawl silently
- The normal audit, improve, repair, build, CI, and MCP-startup paths must be deterministic
  and fully usable offline. Network activity is never implicit.
- Discovery is a separate, opt-in command. Installation triggers no network activity. A
  first-run prompt may *offer* discovery, but the default answer is no.
- All discovered web content is untrusted, hostile data. It is sanitised, size-limited, and
  never executed or allowed to trigger tool calls or status changes. Malicious instructions in
  page text remain inert.

### Why installed copies cannot write to the central registry
- An installed copy can discover and review sources locally, but it cannot push to the central
  Motif registry. The only path upstream is a contribution **bundle** or a **pull request** to
  the contributor's own fork, which the user must explicitly create and confirm.
- Central CI validates submissions (schema, duplicates, canonical URLs, licence evidence,
  malicious text, prompt injection, suspicious scripts, prohibited files, PII/secrets, local
  path leaks). CI may *recommend* a status, but a human maintainer must approve.
- Registry updates to installed copies come only from an official, checksum/signature-verified
  Motif release, applied atomically with rollback. Updates never run during audit or repair.

### Why discovered sources are not trusted automatically
- Every discovered source enters quarantine and cannot be recommended, installed, imported,
  used by build/improve, or contributed until reviewed. Registry inclusion is not endorsement.
- Verified fields require primary-source evidence; marketing claims are never copied into them.

## Consequences
- Safety and determinism are preserved; the feature is usable offline with the seed snapshot.
- Live discovery, automated verification, and implementation-agent handoff remain experimental
  and gated, reflected honestly in the capability matrix.
- Contribution requires explicit user action, protecting privacy and the shared registry.
