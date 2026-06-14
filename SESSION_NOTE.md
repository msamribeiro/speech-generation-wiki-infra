# Session Note — 2026-06-13 (session 46)

Temporary note for resuming ingest tomorrow. Delete after use.

---

## Current state

- **251 ingested, 251 integrated** (passes 1–10 complete)
- **Next integration pass (11)** due after ~25 more papers
- **Standard corpus**: 699 ready, starting from `2509.04093` onwards (chronological)
- **Tier 1 CD**: 43 remaining (top: Fish-Speech 35×, MiniMax-Speech 34×, Mini-Omni2 34×)
- **Tier 2 CD**: 44 remaining (lightweight stubs)

---

## Ingest procedure (standard corpus, 2 at a time)

### Step 1 — Select candidates

```python
python3 -c "
import json, pathlib

papers = []
for f in sorted(pathlib.Path('raw/metadata').glob('*.json')):
    d = json.loads(f.read_text())
    if d.get('status') != 'accepted':
        continue
    if d.get('discovery_source') == 'citation-discovery':
        continue
    papers.append((d.get('published_date',''), d['id'], d.get('title','')[:60]))

papers.sort()
for pd, pid, title in papers[:10]:
    print(f'{pd}  {pid:35s}  {title}')
"
```

Show first 4–6 to user for approval (two pairs of 2). User picks from the list.

### Step 2 — Ingest one pair

Invoke the ingest orchestrator with the approved IDs:

> `speech-generation-ingest-orchestrator`: "Ingest papers {id1} and {id2}. Use the standard ingest workflow. Paper pages only — do not update concept pages."

### Step 3 — Quality check after each pair

```bash
WIKI=/Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content

# Check for disallowed callout types in new pages
grep -n "\[!note\]\|\[!warning\]" $WIKI/papers/{id1}.md $WIKI/papers/{id2}.md

# Check for paper-internal labels leaking
grep -n "Factor [A-C]" $WIKI/papers/{id1}.md $WIKI/papers/{id2}.md

# Check for citation count phrases
grep -n "cited by [0-9]" $WIKI/papers/{id1}.md $WIKI/papers/{id2}.md

# Check for em dashes
grep -n " — " $WIKI/papers/{id1}.md $WIKI/papers/{id2}.md

# Check for "SCA" in prose (should be "spoken conversational agents")
grep -n '\bSCA\b' $WIKI/papers/{id1}.md $WIKI/papers/{id2}.md | grep -v "^[0-9]*:task:\|^[0-9]*:  - SCA"

# Check for adoption claims
grep -in "de facto\|dominant\|widely adopted\|state of the art" $WIKI/papers/{id1}.md $WIKI/papers/{id2}.md
```

Fix any issues before moving to the next pair.

### Step 4 — Repeat for second pair, then next batch

After each batch of ~25 total: run integration pass.

---

## Tier 1 CD ingest procedure

Same as above but use a different candidate query:

```python
python3 -c "
import json, pathlib

papers = []
for f in sorted(pathlib.Path('raw/metadata').glob('*.json')):
    d = json.loads(f.read_text())
    if d.get('status') != 'accepted':
        continue
    if d.get('discovery_source') != 'citation-discovery':
        continue
    if d.get('ingest_tier') != 1:
        continue
    cites = d.get('corpus_citation_count', 0)
    papers.append((cites, d['id'], d.get('title','')[:60]))

papers.sort(reverse=True)
for c, pid, title in papers[:10]:
    print(f'{c:3d}x  {pid:35s}  {title}')
"
```

Invoke the same ingest orchestrator. These use the full standard page template.

---

## Callout rules (quick reference)

| Callout | When |
|---------|------|
| `> [!abstract]` | Abstract card only (top of every paper page) |
| `> [!important]` | Field Significance — **foundational papers only** |
| `> [!tip]` | Field Significance — **high significance** |
| `> [!warning]` | Limitations — **critical limitation only** |
| `> [!note]` | **Never** — convert to prose |

---

## Integration pass invocation

After every ~25 ingested papers:

> `speech-generation-integration-agent`: "Run integration pass on the last 25 ingested papers. Update concept pages, add cross-links, update evidence digests, venue pages, and overview."

---

## Session wrap-up checklist

1. Commit wiki content repo: `git add -A && git commit -m "..."  && git push`
2. Commit infra repo (metadata + logs + STATUS.md): `git add -A && git commit -m "..." && git push`
3. Bump infra submodule: `git submodule update --remote wiki && git add wiki && git commit -m "Update wiki submodule (...)" && git push`
4. Bump site submodule: `cd site && git submodule update --remote && git add content && git commit -m "..." && git push`
5. Verify: `git submodule status` hash == `cd wiki-content && git rev-parse HEAD`
6. Update `memory/project_corpus_status.md` and `memory/MEMORY.md`
7. Delete this SESSION_NOTE.md
