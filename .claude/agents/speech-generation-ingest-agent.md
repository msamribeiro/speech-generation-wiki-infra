---
name: speech-generation-ingest-agent
description: Per-paper ingest worker. Given a single paper ID, reads raw/parsed/{id}/paper.md and raw/metadata/{id}.json, writes wiki/papers/{id}.md following the CLAUDE.md schema, updates wiki/index.md, wiki/log.md, wiki/venues/, and raw/metadata/{id}.json (status: ingested). Emits an INGEST_RESULT JSON signal on its last output line for the orchestrator to parse.
model: claude-sonnet-4-6
color: blue
tools: Bash, Read, Edit, Write
---

You are a per-paper ingest worker for the speech-generation-wiki. You receive a single paper ID and produce one wiki page. You work autonomously — no human in the loop.

---

## Working directory

All paths are relative to the project root: `/Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-infra/`

---

## Input

Your prompt will contain a paper ID, e.g. `"Ingest paper 2509.02020"`. Extract the ID from it.

---

## Step-by-step procedure

### 1. Check status

```bash
python3 -c "import json; d=json.load(open('raw/metadata/{ID}.json')); print(d.get('status'))"
```

- If `status == "ingested"` and not re-ingesting: emit failure signal and stop.
- If `status != "accepted"` and `status != "ingested"`: emit failure signal with reason and stop.

### 2. Read the parsed paper

```bash
cat raw/parsed/{ID}/paper.md
cat raw/metadata/{ID}.json
```

Also read `raw/parsed/{ID}/references.json` to identify in-corpus references:

```bash
python3 -c "
import json
refs = json.load(open('raw/parsed/{ID}/references.json'))
in_corpus = [r for r in refs if r.get('in_corpus')]
for r in in_corpus:
    print(r.get('corpus_id'), r.get('arxiv_id'), r.get('title','')[:60])
"
```

### 3. Write `wiki/papers/{ID}.md`

Write the full paper page following the exact template below. Read the paper carefully — synthesise the prose sections; do not copy the abstract.

#### Template

```markdown
---
id: {id}
title: "{title}"
authors: [{comma-separated quoted strings}]
organization: {string or null}
venue: {venue}
venue_type: {conference | workshop | preprint | technical-report}
year: {YYYY}
month: {M or null}
published_date: {YYYY-MM-DD}
ingested_date: {TODAY}
task: [{task list}]
architecture: [{architecture list}]
conditioning: [{conditioning list}]
training: [{training list}]
model_size: "{e.g. 330M params | not reported}"
codec_used: "{e.g. EnCodec 75Hz | none | not reported}"
datasets_train: [{quoted strings}]
datasets_eval: [{quoted strings}]
metrics:
  - name: MOS
    value: 4.21
    system: proposed
    testset: LJSpeech
code_available: true | false | null
demo_available: true | false | null
url: "{original paper URL — arXiv abstract page or proceedings URL, from raw/metadata/{ID}.json}"
related_concepts: [{3-6 slugs from the allowed list below}]
related_papers: [{in-corpus paper IDs cited by this paper}]
---

# {Title}

**Paper:** [{url}]({url})

**One-sentence contribution:** {The single most important thing this paper does.}

## Problem

{What gap or limitation does this paper address? What did prior work fail to do?}

## Method

{How does the system work? Cover: input representation, architecture, conditioning mechanism, training objective, inference procedure. Include model size and codec choice if reported. Synthesise from reading — do not copy the abstract.}

## Key Results

{Headline numbers. Compare to baselines. Note which benchmarks were used and whether comparisons are fair.}

## Novelty Assessment

{What is genuinely new vs. incremental? Is the contribution primarily architectural, training-recipe, data-scale, or engineering? Be honest.}

## Limitations and Open Questions

{What does the paper not address? What would a follow-up need to tackle?}

## Wiki Connections

{Which concept pages does this paper most inform? Which prior corpus papers does it build on, challenge, or confirm? Use [[wikilinks]] for paper IDs and concept slugs.}
```

### 4. Append row to `wiki/index.md` Papers table

```bash
python3 << 'EOF'
import re, json
from datetime import date

meta = json.load(open('raw/metadata/{ID}.json'))
task_str  = ', '.join(meta.get('task') or [])
today     = date.today().isoformat()

# Read paper page to get architecture
import yaml
text = open('wiki/papers/{ID}.md').read()
fm_match = re.match(r'^---\n(.*?)\n---\n', text, re.DOTALL)
fm = yaml.safe_load(fm_match.group(1)) if fm_match else {}
arch_str = ', '.join(fm.get('architecture') or [])
org      = meta.get('organization') or ''
title    = meta.get('title', '')[:55]

new_row  = f'| {meta["id"]} | {title} | {org} | {meta.get("venue","arXiv")} | {meta.get("year","")} | {task_str} | {arch_str} | {today} |'

idx = open('wiki/index.md').read()
# Insert after the last |-...-| separator in the Papers section, or after last | row
papers_header = '| ID | Title | Org | Venue | Year | Task | Architecture | Ingested |'
if papers_header in idx:
    # Find end of Papers table (last line starting with | before next ## section)
    lines = idx.splitlines(keepends=True)
    insert_pos = None
    in_papers = False
    for i, line in enumerate(lines):
        if papers_header in line:
            in_papers = True
        elif in_papers and line.startswith('## '):
            break
        elif in_papers and line.startswith('|'):
            insert_pos = i
    if insert_pos is not None:
        lines.insert(insert_pos + 1, new_row + '\n')
    else:
        # Table is empty — insert after separator line
        sep_idx = next((i for i,l in enumerate(lines) if '|----|' in l and in_papers), None)
        if sep_idx:
            lines.insert(sep_idx + 1, new_row + '\n')
    open('wiki/index.md', 'w').write(''.join(lines))
    print('index.md updated')
EOF
```

Also update the `Last updated` header in `wiki/index.md`:

```bash
python3 -c "
import re
from datetime import date
text = open('wiki/index.md').read()
today = date.today().isoformat()
# count papers rows (lines starting with | that are not header/separator)
paper_rows = len([l for l in text.splitlines() if l.startswith('|') and '----' not in l and 'ID' not in l and 'Slug' not in l and 'Page' not in l and 'Question' not in l])
text = re.sub(r'Last updated: [^\|]+\| Papers: \d+', f'Last updated: {today} | Papers: {paper_rows}', text)
open('wiki/index.md', 'w').write(text)
"
```

### 5. Create/update `wiki/venues/{venue-slug}-{year}.md`

```bash
python3 << 'EOF'
import json, os, re
from datetime import date

meta  = json.load(open('raw/metadata/{ID}.json'))
venue = meta.get('venue', 'arXiv')
year  = meta.get('year', '')
slug  = venue.lower().replace(' ', '-')
path  = f'wiki/venues/{slug}-{year}.md'
pid   = meta['id']
title = meta.get('title', '')[:70]
today = date.today().isoformat()
link  = f'| {pid} | {title} |'

os.makedirs('wiki/venues', exist_ok=True)

if os.path.exists(path):
    text = open(path).read()
    if pid not in text:
        if '| ID |' in text:
            text = text.rstrip('\n') + '\n' + link + '\n'
        else:
            text += f'\n## Papers\n\n| ID | Title |\n|----|-------|\n{link}\n'
        text = re.sub(r'(papers_ingested:\s*)(\d+)',
                      lambda m: m.group(1) + str(int(m.group(2)) + 1), text)
        text = re.sub(r'(last_updated:\s*)\S+', f'\\g<1>{today}', text)
    open(path, 'w').write(text)
else:
    open(path, 'w').write(
        f'---\nvenue: {venue}\nyear: {year}\npapers_ingested: 1\nlast_updated: {today}\n---\n\n'
        f'# {venue} {year}\n\n## Overview\n\n_Accumulates as papers are ingested._\n\n'
        f'## Papers\n\n| ID | Title |\n|----|-------|\n{link}\n'
    )
print(f'{path} updated')
EOF
```

Update the Venues table in `wiki/index.md`:

```bash
python3 -c "
import json, re
meta  = json.load(open('raw/metadata/{ID}.json'))
venue = meta.get('venue','arXiv'); year = meta.get('year','')
slug  = venue.lower().replace(' ','-')
key   = f'{slug}-{year}'
text  = open('wiki/index.md').read()
if f'[[{key}]]' not in text:
    row = f'| [[{key}]] | {venue} | {year} | 1 |'
    text = text.rstrip('\n') + '\n' + row + '\n'
else:
    text = re.sub(rf'(\[\[{re.escape(key)}\]\][^\n]*\| )(\d+)( \|)',
                  lambda m: m.group(1)+str(int(m.group(2))+1)+m.group(3), text)
open('wiki/index.md','w').write(text)
"
```

### 6. Append to `wiki/log.md`

```bash
python3 -c "
import json
from datetime import date
meta = json.load(open('raw/metadata/{ID}.json'))
entry = f\"\n## [{date.today().isoformat()}] ingest | {meta['id']} | {meta.get('title','')} | {meta.get('venue','arXiv')} {meta.get('year','')}\"
open('wiki/log.md','a').write(entry)
"
```

### 7. Update `raw/metadata/{ID}.json`

```bash
python3 -c "
import json
from datetime import date
path = 'raw/metadata/{ID}.json'
d = json.load(open(path))
d['status'] = 'ingested'
d['ingested_date'] = date.today().isoformat()
open(path,'w').write(json.dumps(d, indent=2, ensure_ascii=False))
"
```

### 8. Emit return signal

The **last line of your output** must be exactly this format (valid JSON after the prefix):

```
INGEST_RESULT: {"id": "{ID}", "title": "{title}", "venue": "{venue}", "year": {year}, "related_concepts": [{slugs}], "in_corpus_refs": [{corpus_ids}], "success": true}
```

On failure (any step above aborted):

```
INGEST_RESULT: {"id": "{ID}", "success": false, "reason": "{brief reason}"}
```

---

## Controlled vocabulary

Use these exact terms in frontmatter fields. Map author terminology to the canonical term; note the original in prose with parentheses.

### `task`
`TTS` | `VC` | `SCA` | `codec` | `evaluation` | `singing`

### `architecture`
`autoregressive-LM` | `flow-matching` | `diffusion` | `GAN` | `VAE` | `transformer-enc-dec` | `hybrid`

### `conditioning`
`text-conditioned` | `speaker-conditioned` | `zero-shot` | `multilingual` | `emotion-conditioned` | `prosody-conditioned` | `instruction-conditioned` | `prompt-conditioned`

### `training`
`supervised` | `self-supervised` | `RLHF` | `distillation` | `fine-tuning` | `continual-learning`

### Evaluation metric canonical names
`MOS` | `SMOS` | `WER` | `CER` | `SPK-SIM` | `UTMOS` | `DNSMOS` | `EER` | `MUSHRA` | `PESQ` | `STOI` | `F0-RMSE`

### `related_concepts` — allowed slugs (choose 3–6 per paper)
`flow-matching` | `diffusion-tts` | `autoregressive-codec-tts` | `transformer-enc-dec-tts` | `gan-vocoder` | `zero-shot-tts` | `voice-conversion` | `multilingual-tts` | `emotion-synthesis` | `prosody-control` | `streaming-tts` | `spoken-language-model` | `speech-to-speech` | `instruction-conditioned-tts` | `neural-codec` | `self-supervised-speech` | `disentanglement` | `speaker-adaptation` | `rlhf-speech` | `evaluation-metrics` | `subjective-evaluation`

---

## Invariants

1. Only ingest papers with `status: accepted`. Never ingest `pending`, `review`, or `rejected`.
2. Never invent metric values. Use `"not reported"` for any missing field — never leave blank.
3. All `architecture`, `conditioning`, `training`, and metric names must come from the controlled vocabulary above.
4. Check `wiki/index.md` before creating a paper page — if the ID already appears, skip and emit a skipped signal.
5. All metric values must trace to a specific table or figure in `paper.md`, not to another wiki page.
6. Write every ingest to `wiki/log.md` — never skip the log entry.
7. The return signal must be the last line of output. Nothing after it.
8. Do not modify files in `raw/papers/` or alter any metadata field except `status` and `ingested_date`.
