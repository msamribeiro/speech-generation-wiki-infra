# Q2 2026 Integration Session

- **Opened:** 2026-11-28
- **Status:** Preflight. The manifest is pending and Phase 1 has yet to begin.
- **Evidence window:** April 1 through June 30, 2026, inclusive, by canonical `published_date`.
- **Snapshot baseline cutoff:** March 31, 2026.

This record tracks the second-quarter integration of speech-generation evidence after the published
Q1 release. Use the [integration protocol](../integration-protocol.md) for each stage and the
[archived Q1 log](2026-11-08-q1-2026-integration-sessions.md) for the previous cycle's decisions.

## Starting scope

A read-only manifest preview against content `cc9ca89` and infrastructure `1ce79a5` reported
no manifest validation errors. These counts describe the checked revisions. Recompute them in
the reused integration worktrees after the date audit.

| Measure | Preview |
|---|---:|
| Eligible paper pages | 174 |
| Pages with canonical concept assignments | 172 |
| Intentionally unassigned pages | 2 |
| Metadata records pointing to an earlier canonical page | 1 |
| Affected concepts | 23 |
| Candidate memberships | 623 |
| Memberships already present | 0 |
| Phase 1 queue | 623 |

The unassigned pages are Saar-Voice (`2604.11803`) and the global prosodic embedding study
(`2606.14004`). Their empty concept assignments were accepted during ingestion. The ICLR record
`iclr-2026-kYkfCs4ZAH` points to the Q4 2025 page `2510.00981` and contributes no Q2
membership. See the [Q2 ingestion archive](2026-11-01-q2-2026-ingestion-sessions.md).

## Preflight and first batch

1. Reuse `speech-generation-wiki-content-q1-integrate` and
   `speech-generation-wiki-infra-q1-integrate`. When Q2 preflight begins, check that both are
   clean, start Q2 branches from the current released main commits in those directories, and
   record both starting commits. Resolve the content checkout explicitly for validation.
2. Audit canonical dates, verified later versions, catalog entries, duplicate pointers, and
   concept assignments. Use the claim-membership freeze rule for papers already integrated.
   Coordinate any paper or metadata corrections with ingestion so each change is made once.
3. Run the full health suite and generate the Q2 manifest twice to confirm it is reproducible.
   Record the frozen manifest path, digest, counts, and approved concept order here.
4. Begin Phase 1 in oldest-first batches of up to 20 papers per concept. Run Phase 2 when each
   concept's Phase 1 queue closes. Record batch IDs, counts, validation, and the next step in this
   session log.
5. After both phases close, follow the Q1 review protocol for cross-concept reconciliation,
   rendering, snapshot, report, and release.

## Session log

### 2026-11-28

Opened the Q2 record and verified the provisional queue against released Q1 content. The next
session will reuse the existing integration worktrees for the canonical-date audit and manifest.
