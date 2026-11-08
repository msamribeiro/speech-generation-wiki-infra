# Peer-Reviewed Version Migration

**Prepared:** 2026-11-08

**Owner:** current Codex session (`/root`); sole owner until the migration is merged

**Status:** Q1 execution batch validated; content released; infrastructure release pending

**Infrastructure base:** `5bea40d` (`main`)

**Content base:** `416ccd6` (`main`)

**Infrastructure branch/worktree:** `work/peer-reviewed-versions` / `speech-generation-wiki-infra-peer-reviewed`

**Content branch/worktree:** `work/peer-reviewed-versions` / `speech-generation-wiki-content-peer-reviewed`

This record is the authoritative cross-agent handoff for the peer-reviewed-version rule. It exists
because ingestion and integration both depend on the same metadata and paper-page state, but must
not implement or apply the rule independently.

---

## Coordination Gate

Until this record reaches **Status: merged and released**:

- the migration owner is the only agent allowed to change paper-date behavior, peer-reviewed-link
  behavior, affected metadata records, or affected published paper pages;
- the ingestion stream may continue PDF download and parsing, but must not write or backfill wiki
  pages, mutate affected metadata/date fields, or change the date/version specifications;
- the Q1 integration stream may audit and plan, but must not create a Q1 integration worktree,
  freeze a Q1 manifest, or write Q1 entries into claim YAMLs; and
- neither stream may cherry-pick part of this migration. Both must consume the same merged content
  and infrastructure commits recorded in the release section below.

If another agent finds this record while the status is not `merged and released`, it should stop
at the relevant write boundary and report the dependency rather than reimplementing the rule.

## Decisions Already Fixed

1. The metadata/page field is `url_peer_reviewed`.
2. A paper is **date-frozen** exactly when its canonical paper ID occurs in the `papers:` list of
   any top-level canonical `_claims/*.yaml` file. No new `date_frozen` metadata field is added.
3. Before integration, a verified conference or journal version fully updates the canonical date,
   year, month, venue, and venue type; the paper may move quarters.
4. After integration, `published_date`, year, and month remain frozen. The summarized-version
   `venue` and `venue_type` also remain on the canonical record so its frozen year is not displayed
   as the peer-reviewed venue year. The later publication is recorded in `peer_reviewed_venue`,
   `peer_reviewed_venue_type`, its supporting conference/journal date, source IDs, and
   `url_peer_reviewed`.
5. The existing `url` continues to identify the version summarized by the page. The new link is
   shown separately, and an italic editorial note states that the page, metrics, and claims
   summarize the ingested version while a peer-reviewed version is available.
6. Claim YAMLs, reconciliation state, published snapshots, and historical reports are not rewritten
   by this migration. Frozen metadata dates must continue to match their existing claim entries.
7. A technical report and substantially rewritten peer-reviewed paper remain separate works under
   the existing VibeVoice precedent; they are not folded into this rule mechanically.

## Preconditions

- [x] Infrastructure and content `main` were inspected and are clean at the recorded base commits.
- [x] The local ingest branches contain no tracked divergence from their corresponding `main`
      branches. Local caches and parsed artifacts in the infra ingest worktree remain untouched.
- [x] Dedicated infrastructure and content migration worktrees were created from `main`.
- [x] The existing metadata schema, date library, migration script, metadata health check, ingest
      skill, integration skill, and integration protocol were inspected.
- [x] This coordination record is committed and made visible to the ingest branch.
- [ ] A deterministic dry-run manifest is generated and reviewed before any apply operation.
- [ ] Every conference/journal date and peer-reviewed URL in the manifest has an authoritative
      source recorded; inferred dates are not allowed.

## Current Implementation Gaps

The current code cannot safely implement the agreed rule:

- `lib/paper_dates.py` always lets `conference_date`/`journal_date` replace `published_date`; it
  has no caller-controlled frozen-date mode.
- `scripts/apply_date_rule.py` has only a coarse `--ingested-from` migration and does not inspect
  claim membership, add peer-reviewed links, edit venue/card/note fields, or emit a deterministic
  apply manifest.
- `scripts/checks/metadata.py` treats an ingested frozen date that differs from a later conference
  date as a warning rather than validating the deliberate exception against claim membership.
- the metadata schema's current “Duplicates and Later Versions” prose says all post-ingest pages
  keep their date; it does not distinguish pre-integration from post-integration records.
- ingest/review templates do not expose `url_peer_reviewed` or the editorial note.
- there are no focused tests for frozen detection, page transformation, deterministic manifests,
  or idempotence.

## Phase 1 Inventory Checkpoint — 2026-11-08

The read-only inventory is `docs/records/2026-11-08-peer-reviewed-version-inventory.json`,
generated by `scripts/audit_peer_reviewed_versions.py` against the dedicated content checkout.
Its initial SHA-256 is
`08ef8b754dbfef01f299612dccc6011ad9d34d2291007896f702e07b597a1a00`.

Initial conservative discovery results:

- 261 active canonical preprint candidates;
- 88 already integrated and therefore date-frozen;
- 127 with an explicit ISCA, ACL Anthology, or OpenReview source identifier;
- 194 with an acceptance/publication comment (some also have source IDs);
- 134 comment-only candidates whose identity and landing page remain unverified;
- 139 candidates missing a verified peer-reviewed date; and
- 145 unresolved overall.

This broad inventory intentionally includes historical and future-quarter discoveries. It is not
the apply manifest. Phase 1 must classify the 261 entries into the authorized backfill, already
correct/no-op, technical-report exception, rejected/duplicate support record, deferred legacy
backfill, or unresolved identity/date/URL before Phase 2 can create an apply plan.

## Execution Plan

### Phase 1 — Specify the contract and build the inventory

1. Reconcile the rule in `docs/schemas/metadata.md`, `docs/schemas/generation.md` if necessary,
   `docs/content.md`, `docs/ingest-protocol.md`, and `docs/integration-protocol.md`.
2. Update the ingest, lightweight-ingest, and review skills so newly written pages use the rule
   without a later repair pass.
3. Build one deterministic membership index from the canonical content checkout's top-level claim
   YAMLs. Exclude `_claims/_reconciliation/` from frozen detection.
4. Build a candidate inventory from metadata and verified source IDs rather than from the backlog's
   hand-maintained list. The inventory must still explicitly reconcile every known class:
   - re-dated and not-yet-ingested Interspeech 2026 records;
   - the 34 existing Q3 Interspeech pages;
   - the 10 integrated Q3/Q4 2025 pages later published at Interspeech 2026;
   - ICASSP 2026 records using the confirmed start date `2026-05-03`;
   - ICML 2026 (`2026-07-06`) and IJCAI 2026 records, including the two held records;
   - ACL 2026, AAAI-26, ICME, ICPR, Speech Prosody, and LREC records;
   - integrated ASRU 2025 and SLT 2024 records; and
   - later journal versions and technical-report exceptions surfaced by the same scan.
5. For each candidate record, capture: canonical ID, old/new venue fields, supporting date field,
   old/proposed canonical date and quarter, frozen concepts (if any), existing and peer-reviewed
   URLs, source IDs, page existence, and intended page operation.

**Gate:** inventory has no unresolved date, identity, URL, or technical-report classification.

### Phase 2 — Implement one migration path

1. Add an explicit preserve-date option to the shared date-rule API. Content/claim membership is
   resolved by the migration/checking layer and passed into the library; `lib/paper_dates.py` must
   not reach into the content repository implicitly.
2. Implement a dedicated peer-reviewed-version migration entry point rather than overloading the
   historical bulk date migration. It must accept an explicit `--wiki-dir`, default to dry run,
   require an explicit apply flag, and emit a stable machine-readable manifest.
3. Make page edits surgical and repeatable:
   - update frontmatter venue/date fields according to frozen status;
   - add or update `url_peer_reviewed` once;
   - keep the original `url`;
   - update the abstract card's venue/link presentation;
   - add exactly one canonical editorial note; and
   - update the paper catalog row without duplicating it.
4. Update metadata health so:
   - non-integrated records remain strict under the canonical date priority;
   - integrated frozen records may retain their existing canonical date only when claim membership
     proves the freeze;
   - year/month match the retained date; and
   - supporting dates and URLs remain fully validated.
5. Add focused unit tests for date preservation, claim-membership detection, frozen/non-frozen
   health behavior, page transformation, deterministic manifest output, and a no-op second apply.

**Gate:** tests pass and the dry-run manifest is stable across two consecutive runs.

### Phase 3 — Review the dry-run manifest

Before applying, review and record:

- exact record and page counts by operation;
- quarter movement counts, especially Q1→Q2 and Q2→Q3;
- frozen record count and the concepts proving each freeze;
- records missing pages, peer-reviewed URLs, venue dates, or source identifiers;
- duplicate/canonical-ID decisions; and
- the resulting provisional Q1 paper and concept-membership counts.

No mutation is allowed while any manifest entry is unresolved. The reviewed manifest digest is
recorded in this file.

### Phase 4 — Apply once in the dedicated worktrees

1. Apply the reviewed manifest to infra metadata and the dedicated content checkout only.
2. Append one infra pipeline-log entry and one content `misc` log entry summarizing the migration.
3. Do not edit claim YAMLs, reconciliation files, snapshots, concept renders, or reports.
4. Run the migration again in dry-run mode. It must report zero changes.

**Gate:** second dry run is a no-op and `git diff` matches the reviewed manifest exactly.

### Reviewed Q1 execution batch (2026-11-08)

The first bounded execution batch is the Q1 preflight dependency recorded in
`2026-11-08-q1-peer-reviewed-versions.yaml`. Two independent dry runs produced the same manifest:

- manifest SHA-256: `4f68061ab59326f0dcbe1e4de27d5b8ae68e27f45041fda75df44cc39cc7460c`;
- 20 verified records, 20 metadata changes, 20 page changes, and 20 catalog-row changes;
- zero frozen records (none of the IDs occurs in a top-level canonical claim YAML);
- 18 quarter moves: 16 Q1 2026 to Q2 2026, one to Q4 2025, and one to Q4 2024;
- two AAAI records remain in Q1 2026; and
- two records are explicitly deferred: `2603.19831` is an explicitly non-archival workshop paper,
  while `2603.24144` lacks an exact authoritative ICME proceedings record.

This batch changes no claim YAML, reconciliation state, snapshot, concept render, or report.
After application, the repeat dry-run manifest SHA-256 was
`0185d2f26c43234bb83518e9a39a38ab5b5106f56c03ac9ef635ab8d84711688` and reported zero metadata,
page, catalog, or quarter changes. The full 53-test suite and all six health modules passed. The
resulting Q1 set is 116 ingested pages: 105 arXiv, nine workshop, and two AAAI records; none is yet
present in a top-level claim YAML.

### Phase 5 — Validate

Run, against the explicit migration content checkout:

1. focused unit tests;
2. agent compatibility health after skill/protocol changes;
3. metadata, ingest, integrate, reconcile, and render health modules;
4. the full health suite;
5. exact page/index uniqueness checks;
6. an audit proving `_claims/`, reconciliation, snapshots, and reports are unchanged; and
7. a fresh Q1 bounded audit using the final canonical dates.

All health modules must have zero errors. Warning deltas must be explained in this record rather
than accepted silently.

### Phase 6 — Commit, merge, and release

1. Commit the content migration independently and record its SHA.
2. Commit infra code, metadata, tests, schemas, skills, logs, and this completed record; record its
   SHA and the reviewed manifest digest.
3. Merge content first into content `main`.
4. Validate the merged content checkout from infra.
5. Merge infra into infra `main` and update the content submodule pointer only after the content
   commit is present on `main`.
6. Merge the resulting mainline commits into the ingest worktrees. Create the Q1 integration
   worktrees only from these released commits.
7. Change this record to **Status: merged and released**, update `STATUS.md` and `BACKLOG.md`, and
   record the two release SHAs below.

## Release Record

- Reviewed manifest path: `docs/records/2026-11-08-q1-peer-reviewed-versions.yaml`
- Reviewed manifest SHA-256: `4f68061ab59326f0dcbe1e4de27d5b8ae68e27f45041fda75df44cc39cc7460c`
- Content migration commit: `844fb57`
- Infrastructure migration commit: `e90a717`
- Content `main` merge commit: `844fb57` (fast-forward)
- Infrastructure `main` merge commit: _pending_
- Post-content-merge health baseline: all six modules pass; zero errors
- Final canonical Q1 page count: 116
- Final canonical Q1 concept-membership count: 453 across 22 concepts

## Downstream Release Conditions

The ingestion agent may resume page writes only after it verifies that its content and infra bases
contain the recorded release commits. The integration agent may create the Q1 worktrees and freeze
the Q1 manifest only after the same verification and after recomputing the quarter from canonical
metadata. Neither agent may reuse the provisional pre-migration Q1 counts.
