# Ingest Optimization Experiment — Direct Agent Invocation

**Status:** Temporary experiment file. Remove once the approach is validated and folded into the standard workflow.

**Goal:** Test whether dropping the `speech-generation-ingest-orchestrator` subagent and invoking `speech-generation-ingest-agent` workers directly in parallel from the main session meaningfully reduces token consumption per ingest batch.

**Background:** The orchestrator adds ~130k tokens of coordination overhead per 5-paper batch (it loads CLAUDE.md fresh, discovers papers, spawns agents, and collects results — all as a subagent with its own context window). When papers are manually selected upfront, the orchestrator provides no value over direct invocation.

---

## Override: how to run an ingest batch in this experiment

Instead of:
```
→ speech-generation-ingest-orchestrator: "Ingest up to 5 papers"
```

Do the following directly in the main session:

### Step 1 — Select papers

Run this to find the top accepted, parsed, not-yet-ingested papers by relevance score (filter by task if desired):

```bash
source .venv/bin/activate && python3 - <<'EOF'
import json, os, glob

candidates = []
for f in glob.glob("raw/metadata/*.json"):
    with open(f) as fh:
        m = json.load(fh)
    if m.get("status") != "accepted":
        continue
    pid = m.get("id", "")
    if not os.path.exists(f"raw/parsed/{pid}/paper.md"):
        continue
    tasks = m.get("task", [])
    if isinstance(tasks, str):
        tasks = [tasks]
    candidates.append({
        "id": pid,
        "title": m.get("title", ""),
        "relevance_score": m.get("relevance_score", 0),
        "task": tasks,
        "venue": m.get("venue", ""),
        "year": m.get("year", ""),
    })

candidates.sort(key=lambda x: x["relevance_score"], reverse=True)
print(f"{'ID':<45} {'Score':>6}  {'Task':<25} {'Venue':<12} {'Year'}  Title")
print("-" * 130)
for c in candidates[:15]:
    print(f"{c['id']:<45} {c['relevance_score']:>6.2f}  {str(c['task']):<25} {c['venue']:<12} {c['year']}  {c['title'][:50]}")
EOF
```

Pick 5 papers. Present the list to the user for confirmation before proceeding.

### Step 2 — Spawn 5 ingest agents in parallel

In a **single message**, launch all 5 `speech-generation-ingest-agent` subagents simultaneously. Each agent handles exactly one paper. Pass the paper ID explicitly so the agent does not need to do any discovery.

Each agent prompt should be:

> Ingest paper `{id}`. Read `raw/parsed/{id}/paper.md`, `raw/parsed/{id}/metadata.json`, and `raw/parsed/{id}/references.json`. Write the wiki paper page at `wiki/papers/{id}.md` following the full paper page template in CLAUDE.md. Then: update `wiki/index.md` (add one paper row), append one ingest bullet to `wiki/log.md` under today's date, update `wiki/venues/{venue-year}.md`, and set `status: ingested` and `ingested_date: {today}` in `raw/metadata/{id}.json`. Do NOT update concept pages. Emit INGEST_RESULT on last line: `{"ingested": ["{id}"], "failed": [], "skipped": []}`.

Substitute `{id}`, `{venue-year}`, and `{today}` for each paper.

### Step 3 — Verify

After all 5 agents complete, run:

```bash
for id in <id1> <id2> <id3> <id4> <id5>; do
  st=$(python3 -c "import json; m=json.load(open('raw/metadata/$id.json')); print(m.get('status','?'), m.get('ingested_date','?'))")
  lines=$(wc -l < "wiki/papers/$id.md" 2>/dev/null || echo "MISSING")
  echo "$id  $st  lines=$lines"
done
```

All 5 should show `ingested <date>` with page line counts in the 90–130 range.

### Step 4 — Update STATUS.md

Update the ingest count and metadata counts section in `STATUS.md` to reflect the new totals.

---

## What to measure

After running a batch with this approach, note in this file:

- Total tokens consumed (check session usage)
- Any index.md / log.md write conflicts (parallel agents may race on shared files — if so, fall back to sequential invocation or a post-batch cleanup pass)
- Quality of wiki pages produced vs. orchestrator-produced pages (spot-check one or two)

---

## Known risk: shared file write conflicts

`wiki/index.md`, `wiki/log.md`, and venue pages are written by every agent. When 5 agents run in parallel, there is a risk that agents clobber each other's edits on these shared files. If this happens:

**Mitigation A (simplest):** Run agents sequentially (one at a time) instead of in parallel. Still saves orchestrator overhead (~130k tokens); loses parallelism speedup.

**Mitigation B:** Have each agent skip shared file updates (index, log, venue) and perform a single batch update pass in the main session after all paper pages are written.

Start with parallel execution and inspect the shared files after the run. If conflicts appear, switch to Mitigation A.
