# Review Session Context

Temporary working document for the ongoing health-check review pass. Delete when all flagged papers are cleared.

See `memory/project_health_check_review_pass.md` for the durable version of this context.

---

## Task

Fix all pages failing `scripts/health_check.py --module ingest`. Two error classes:

- **`required_fields`** — missing `field_significance` frontmatter block
- **`claims_section`** — missing `## Claims` section, or claim bullets lack `*(§N.N)*` citations

Current scope: all venues — Interspeech 2025, ACL/EMNLP/NAACL/COLING, and arXiv.

---

## Approach

For each batch of 2 papers:

1. **Snapshot** current files before any changes:
   ```bash
   cp /path/to/speech-generation-wiki-content/papers/{ID}.md /tmp/{ID}.before.md
   ```

2. **Run review agent** (`speech-generation-review-agent`) on each paper sequentially — never in parallel. Wait for each to finish before starting the next.

3. **Diff** the before and after to inspect every change:
   ```bash
   diff /tmp/{ID}.before.md /path/to/speech-generation-wiki-content/papers/{ID}.md
   ```

4. **Summarise and critique the diff.** Look for:
   - Hallucinated metric values or section references
   - Wrong `field_significance.type` (common: `architectural-novelty` applied to `engineering-integration` papers)
   - Wrong or missing `related_concepts` additions/removals
   - Bare wikilinks in newly added Wiki Connections prose (see Helper Notes below)
   - Figure embeds on Interspeech papers (see Helper Notes below)

5. **Fix any issues** found in the diff before running the health check.

6. **Health check** against the standalone content repo — no commit or push needed:
   ```bash
   WIKI=/Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content
   .venv/bin/python scripts/health_check.py --module ingest --id {ID} --wiki-dir "$WIKI" -v
   ```

7. **Stop and report** — summarise changes, flag concerns, wait for go-ahead before next batch.

---

## Helper Notes

### Bare wikilinks (recurring agent blind spot)
The review agent adds paper IDs to `related_papers` and writes about them in Wiki Connections prose, but uses bare `[[id]]` or `[[id]] (Name)` format instead of `[[id|Name]]`. After every diff, grep for bare wikilinks in the modified file:
```bash
grep "\[\[[0-9]\|interspeech\|acl\|emnlp\|naacl" /path/to/content/papers/{ID}.md | grep -v "|"
```
**Rule:** use `[[id|Name]]` when a clean display name exists (model name, system name). Bare `[[id]]` is acceptable when no clean name applies. Never write `[[id]] (Name)`.

The agent spec was patched on 2026-06-20 to document this rule. Watch for recurrence.

### Interspeech figure sanity
Docling typically assigns `figure-1.png` to the ISCA logo on Interspeech papers. If the review agent embeds a figure from an Interspeech paper, check file sizes in `raw/parsed/{ID}/assets/` — the logo is the smallest file. Flag for manual visual verify before any site bump.

```bash
ls -lh raw/parsed/{ID}/assets/*.png
```

The smallest file is usually the logo. The agent should embed the largest figure whose caption matches the architectural selection criteria.

### F5-TTS paper ID
F5-TTS's canonical wiki ID is `2025.acl-long.313` (ACL 2025), **not** `2410.06885` (arXiv). Pass this note to the review agent prompt when the paper is likely to cite F5-TTS. Always verify `related_papers` IDs against the wiki index.

### `--wiki-dir` flag
Added to `scripts/health_check.py` on 2026-06-20. Lets you validate changes against the standalone content repo without committing to the submodule or pushing to GitHub.

```bash
WIKI=/Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content
.venv/bin/python scripts/health_check.py --module ingest --wiki-dir "$WIKI"
```

---

## Remaining candidates — 72 papers (updated 2026-06-23)

Draw from all three groups; mix venues across sessions for topic diversity.

### Interspeech 2025 — 0 papers

*(all Interspeech 2025 papers complete)*

### NLP venues (ACL/EMNLP/NAACL/COLING) — 17 papers

```
2025.acl-long.682     2025.acl-long.911     2025.acl-long.912     2025.acl-short.81
2025.americasnlp-1.1  2025.ccl-1.80         2025.coling-main.352  2025.coling-main.518
2025.emnlp-demos.70   2025.emnlp-main.1730  2025.emnlp-main.180   2025.emnlp-main.989
2025.findings-acl.1051  2025.findings-emnlp.424  2025.findings-naacl.184  2025.naacl-long.110
2025.naacl-long.242
```

### arXiv — 55 papers

```
2507.22746  2508.00317  2508.01796  2508.02013  2508.02038  2508.02849  2508.03543
2508.04141  2508.04585  2508.04996  2508.05207  2508.05385  2508.06262  2508.06870
2508.06890  2508.07302  2508.07426  2508.07711  2508.08095  2508.08399  2508.08715
2508.08961  2508.09767  2508.11273  2508.11326  2508.12001  2508.14049  2508.15442
2508.15827  2508.16332  2508.19098  2508.20660  2509.00685  2509.02020  2509.09631
2509.15969  2509.19668  2510.00981  2510.02848  2510.05758  2510.07979  2510.12210
2511.12347  2512.04720  2512.13251  2512.14291  2601.03888  2601.15621  2603.08823
2603.18090  2603.26364  2603.29339  2604.00688  2604.01760  2604.12438
```

To resume: proceed in batches of 4.
