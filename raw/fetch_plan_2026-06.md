# Corpus Top-Up Fetch Plan — June 2026

**Goal:** Fully cover 2025-07-01 → 2026-05-31 for all three categories. cs.SD + eess.AS was already re-scanned with the expanded keywords on 2026-05-25 (that was the "70 re-scan" in STATUS.md), so it only needs a July 2025 backfill and a May 25–31 tail. cs.CL was scanned with the old keyword list and needs a full re-scan for Aug 2025–May 2026 plus the July 2025 backfill. Keyword expansion: +11 terms added 2026-05-25.

**Prerequisite:** Activate the virtualenv before every session.
```bash
source .venv/bin/activate
```

---

## Batches

| ID | Category | Window | Status | Notes |
|----|----------|--------|--------|-------|
| A1 | cs.SD | 2025-07-01 → 2025-07-31 | complete | July backfill; OAI-PMH (search API rate-limited) |
| A2 | eess.AS | 2025-07-01 → 2025-07-31 | complete | July backfill; OAI-PMH |
| B | cs.CL | 2025-07-01 → 2025-07-31 | complete | July backfill; new window, never scanned |
| C | cs.CL | 2025-08-01 → 2025-11-30 | complete | Re-scan with expanded keywords; ~9,461 records, ~10 OAI pages |
| D | cs.CL | 2025-12-01 → 2026-02-28 | complete | Re-scan with expanded keywords; ~6,857 records, ~7 OAI pages |
| E | cs.CL | 2026-03-01 → 2026-05-31 | complete | Re-scan + new (prev ended 2026-05-22); ~10,000+ records, ~10 OAI pages |
| F1 | cs.SD | 2026-05-25 → 2026-05-31 | complete | May tail; OAI-PMH |
| F2 | eess.AS | 2026-05-25 → 2026-05-31 | complete | May tail; OAI-PMH |

**Why no cs.SD + eess.AS re-scan for Aug 2025–May 2026?** The "70 re-scan" in STATUS.md was already a keyword-expansion re-scan of those categories run on 2026-05-25 (same day as the keyword expansion). Only the July and May-tail windows were missed.

**Estimated total (OAI-PMH batches B–E):** ~28,800 records. At 5s/page (1,000 records/page), ~145s enforced sleep minimum; in practice 1–3 hours depending on server latency and retries. Batches A and F (search API) are fast — minutes each.

---

## Commands

### Batch A — cs.SD + eess.AS, July 2025

**Note:** `arxiv.py` (search API) was rate-limited (429 on all retries). Switched to `arxiv_oai.py` for both categories. Run as two separate commands — OAI-PMH handles one set at a time.

```bash
# cs.SD
python scripts/fetch/arxiv_oai.py --set cs.SD --date-from 2025-07-01 --date-to 2025-07-31 2>&1 | tee raw/fetch_log_A_csSD.txt

# eess.AS
python scripts/fetch/arxiv_oai.py --set eess.AS --date-from 2025-07-01 --date-to 2025-07-31 2>&1 | tee raw/fetch_log_A_eessAS.txt
```

### Batch B — cs.CL, July 2025

New window (never scanned). Small (~3 OAI pages), expected to complete in minutes.

```bash
# Dry run first
python scripts/fetch/arxiv_oai.py --set cs.CL --date-from 2025-07-01 --date-to 2025-07-31 --dry-run

# Execute
python scripts/fetch/arxiv_oai.py --set cs.CL --date-from 2025-07-01 --date-to 2025-07-31 2>&1 | tee raw/fetch_log_B.txt
```

### Batch C — cs.CL, Aug–Nov 2025

Re-scan. Previous run (2026-05-xx) wrote 41 papers from ~9,461 records; those 41 will be skipped. New papers matching the expanded keywords will be written.

```bash
# Dry run first
python scripts/fetch/arxiv_oai.py --set cs.CL --date-from 2025-08-01 --date-to 2025-11-30 --dry-run

# Execute
python scripts/fetch/arxiv_oai.py --set cs.CL --date-from 2025-08-01 --date-to 2025-11-30 2>&1 | tee raw/fetch_log_C.txt
```

### Batch D — cs.CL, Dec 2025–Feb 2026

Re-scan. Previous run wrote 32 papers from ~6,857 records; those 32 will be skipped.

```bash
# Dry run first
python scripts/fetch/arxiv_oai.py --set cs.CL --date-from 2025-12-01 --date-to 2026-02-28 --dry-run

# Execute
python scripts/fetch/arxiv_oai.py --set cs.CL --date-from 2025-12-01 --date-to 2026-02-28 2>&1 | tee raw/fetch_log_D.txt
```

### Batch E — cs.CL, Mar–May 2026

Re-scan + new papers (previous run ended 2026-05-22; this extends to 2026-05-31). Previous run wrote 42 papers.

```bash
# Dry run first
python scripts/fetch/arxiv_oai.py --set cs.CL --date-from 2026-03-01 --date-to 2026-05-31 --dry-run

# Execute
python scripts/fetch/arxiv_oai.py --set cs.CL --date-from 2026-03-01 --date-to 2026-05-31 2>&1 | tee raw/fetch_log_E.txt
```

### Batch F — cs.SD + eess.AS, May 2026 tail

Covers the days missed since the last fetch ended (2026-05-25). Two separate OAI-PMH runs.

```bash
# cs.SD
python scripts/fetch/arxiv_oai.py --set cs.SD --date-from 2026-05-25 --date-to 2026-05-31 2>&1 | tee raw/fetch_log_F_csSD.txt

# eess.AS
python scripts/fetch/arxiv_oai.py --set eess.AS --date-from 2026-05-25 --date-to 2026-05-31 2>&1 | tee raw/fetch_log_F_eessAS.txt
```

---

## Resuming an Interrupted OAI-PMH Run

If a batch is interrupted (network failure, session timeout, rate-limit exhaustion), the script prints a resume token on the last output line before giving up:

```
To resume, rerun with: --resume-token CS6JbWFyazoyMDI1LTA4LTAxfDEwMDA=...
```

**Always pipe output to `tee` (as shown above)** so the token is saved in the log file even if the terminal closes.

To resume:
```bash
python scripts/fetch/arxiv_oai.py --resume-token <token-from-log> 2>&1 | tee -a raw/fetch_log_C.txt
```

No `--date-from` / `--date-to` needed — the token encodes the window. Use `-a` with `tee` to append rather than overwrite the existing log.

**Note:** After a successful resume, the script continues from the interrupted page. Papers already written before the interruption are skipped (idempotent).

**If the resume token is lost:** Safe to re-run the full batch command. The run will re-scan pages already processed but will skip any files already written. Slower, not harmful.

---

## After All Batches Complete

Update the Status column above, then proceed to:

1. **Filter** — run `speech-generation-filter-agent` on all newly written `status: pending` papers.
2. **Human review** — resolve `raw/review_queue.md` borderline papers.
3. **Download PDFs** — `python scripts/parse/download_pdfs.py`
4. **Parse** — `python scripts/parse/batch_convert.py --ids <new_ids>`
5. **Regenerate batch queue** — `python scripts/parse/make_batch_queue.py`

---

## Results Log

Fill in as each batch completes.

| Batch | Run date | Discovered | Passed filter | Written (new) | Skipped (existing) | Errors |
|-------|----------|------------|---------------|---------------|--------------------|--------|
| A1 | 2026-06-05 | 353 | 52 | 52 | 0 | 0 |
| A2 | 2026-06-05 | 401 | 59 | 9 | 50 | 0 |
| B | 2026-06-05 | 1867 | 21 | 3 | 18 | 0 |
| C | 2026-06-05 | 9330 | 127 | 12 | 115 | 0 |
| D | 2026-06-05 | 6579 | 73 | 5 | 68 | 0 |
| E | 2026-06-05 | 10571 | 110 | 13 | 97 | 0 |
| F1 | 2026-06-05 | 94 | 13 | 6 | 7 | 0 |
| F2 | 2026-06-05 | 60 | 13 | 8 | 5 | 0 |
