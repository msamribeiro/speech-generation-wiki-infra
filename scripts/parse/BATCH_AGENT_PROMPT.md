# Batch Conversion Sub-agent Instructions

This document is the complete, self-contained brief for a sub-agent inspecting one batch of
PDF-to-Markdown conversions for the speech-generation wiki.

**IMPORTANT: You do NOT run the conversion.** Conversion is already complete before you are
spawned. Your only job is to inspect the output files and return a quality summary table.
Do not run `batch_convert.py` or any long-running process.

---

## Context

You are checking output quality for a batch of papers from a systematic review wiki of speech
synthesis research. The PDF-to-Markdown pipeline has already been run. You will read the output
files, apply quality checks, and return a compact summary — nothing else.

Do NOT write to the wiki, modify metadata, or perform any action beyond reading files.

---

## Working Directory

All file paths are relative to:

```
/Users/sribeiro/Documents/Coding/speech-generation-wiki
```

---

## Step 1 — Check Each Paper

For each paper ID in your batch brief, inspect `raw/parsed/{id}/`:

### 1a. Success check

Look for `paper.md` (success) or `error.json` (failure). If `error.json` exists, read it
for the error type and message.

### 1b. Line count

Count lines in `paper.md`:

```bash
wc -l raw/parsed/{id}/paper.md
```

Thresholds:
- **Good**: > 80 lines
- **Thin**: 20–80 lines (may be a legitimately short workshop/demo paper — check the title)
- **Broken**: < 20 lines — flag as quality issue

### 1c. Title check

Read the first 8 lines of `paper.md` and check the `title:` field in the YAML frontmatter.
Flag if the value is `"Unknown"`, `null`, or empty string.

### 1d. Section count

```bash
grep -c "^##" raw/parsed/{id}/paper.md
```

Expect 3–10 sections for a typical conference or journal paper. 0 sections on a non-trivial
paper is a quality issue.

### 1e. Table count

```bash
grep -c "^|" raw/parsed/{id}/paper.md
```

Not all papers have tables; 0 is only a concern for result-heavy papers.

### 1f. Reference count

```bash
python3 -c "import json; r=json.load(open('raw/parsed/{id}/references.json')); print(len(r), 'refs,', sum(1 for x in r if x.get('in_corpus')), 'in-corpus')"
```

Expect 10–80 references. Fewer than 5 may indicate a references extraction failure.

**Note on workshop/demo papers:** IDs like `2025.acl-demo.*`, `2025.acl-short.*`,
`2025.americasnlp-*`, `2025.iwsds-*` are often 4–8 page papers. Thin line counts (40–80)
are normal for these — use judgment before flagging.

---

## Step 2 — Return ONLY This

Return exactly the following three sections. No preamble, no explanations, no extra text.

### Section 1: Results Table

```
## Batch {N} Results

| ID | Lines | Sections | Tables | Refs | Title OK | Status | Notes |
|----|-------|----------|--------|------|----------|--------|-------|
| 2509.12345 | 143 | 7 | 12 | 45 | yes | ok | |
| interspeech-2025-0412 | 0 | — | — | — | — | FAILED | ValueError: page count exceeded |
```

Status values:
- `ok` — all checks passed
- `thin` — under 80 lines but appears to be a legitimately short paper
- `FAILED` — `error.json` exists (copy the error type and first line of message)
- `quality-issue` — converted but something suspicious (title Unknown, 0 sections, <5 refs)

### Section 2: Verdict

One line:

```
Verdict: {N}/20 succeeded, {M} failed, {K} quality issues. [One sentence on overall quality.]
```

### Section 3: Needs Attention (omit entire section if none)

```
## Needs Attention
- `2509.99999` — FAILED: MemoryError (PDF may be corrupted)
- `interspeech-2025-0001` — quality-issue: title Unknown, 0 sections extracted
```

---

## Quality Thresholds (reference)

| Metric | Good | Warn | Flag |
|--------|------|------|------|
| Lines  | > 80 | 20–80 | < 20 |
| Sections (`##`) | ≥ 3 | 1–2 | 0 |
| Title | real title | — | "Unknown" / null |
| References | ≥ 10 | 5–9 | < 5 |
