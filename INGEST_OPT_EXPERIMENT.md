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

## Results: primary-session sequential run (2026-05-28)

**Variant run:** Primary-session sequential (no subagents at all). Papers processed one at a time in the main context window.

**Papers:** 2506.21619, 2025.naacl-long.242, 2510.12210, 2025.emnlp-main.40, 2603.08823 — 5/5 ingested, 0 failed.

**Token usage:** No meaningful reduction observed vs. orchestrator-based batches.

**Why:** The primary-session approach saves the ~130k orchestrator overhead, but the main session context accumulates all paper content sequentially — by paper 5, it carries content from all 4 prior papers. These costs roughly cancel out. The per-paper reading cost (paper.md is typically 300–600 lines) dominates regardless of approach.

**Conflict-free writes:** Confirmed. Sequential execution in a single session produces no shared-file write conflicts on `wiki/index.md`, `wiki/log.md`, or venue pages. This was the main practical benefit.

**Page quality:** No difference from subagent-produced pages. Same source data, same instructions.

**Conclusion:** Primary-session sequential ingest is a viable fallback (reliable, no conflicts, no orchestrator needed) but does not achieve meaningful cost savings over the standard orchestrator pipeline.

---

## Results: parallel direct subagents (2026-05-29)

**Variant run:** 5 `speech-generation-ingest-agent` workers spawned simultaneously in a single main-session message, no orchestrator.

**Papers:** 2512.04720, 2509.09631, 2509.00685, 2511.12347, 2512.13251 — 5/5 ingested, 0 failed.

**Token usage per worker:**

| Paper | Tokens | Tool uses | Wall time |
|-------|--------|-----------|-----------|
| 2512.04720 | 63,603 | 31 | ~256s |
| 2509.09631 | 71,659 | 36 | ~274s |
| 2509.00685 | 56,660 | 28 | ~230s |
| 2511.12347 | 68,607 | 28 | ~216s |
| 2512.13251 | 71,316 | 24 | ~232s |
| **Total** | **331,845** | **147** | **~274s (parallel wall time)** |

**Comparison to orchestrator approach (estimated):**
- Orchestrator: ~130k (coordination) + 5 × ~37.5k (workers) = ~317k total
- Parallel direct: ~332k total subagent tokens, ~0 main-session accumulation
- Net difference: roughly equivalent token cost, but direct approach saves the ~130k orchestrator context from loading into the main session.

**Shared-file write conflicts:** Races observed on integer counter fields. Agents reported `Papers:` counts of 45, 47, 48, 49 for `wiki/index.md` and `papers_ingested` values of 19, 20, 21 for `wiki/venues/arxiv-2025.md`. Final values were correct (49 and 21 respectively) — the last writer happened to hold the right count. No paper rows or log bullets were lost: all 5 paper rows appear in `index.md`, all 5 ingest bullets appear in `wiki/log.md`, and all 4 arXiv venue rows appear in `arxiv-2025.md`.

**Why no row loss despite race conditions:** Each agent uses the Edit tool's find-and-replace to append rows to tables (finding the last row and inserting after it), rather than overwriting the whole file. This makes row additions near-atomic; two agents appending different rows at different table positions do not clobber each other. Counter updates (the `Papers: N` header and `papers_ingested: N` frontmatter) are simple integer replacements — whichever agent writes last wins, but with N agents all adding 1 from slightly staggered reads, the final result is correct if and only if each agent sees the prior agent's write before its own. This happened to hold here, but is not guaranteed.

**Page quality:** No difference from orchestrator-produced pages. Same source data, same agent spec.

**Conclusion:** Parallel direct subagents is viable in practice. Token cost is comparable to the orchestrator (slightly higher per-worker cost offset by no orchestrator overhead). The main advantage is wall time (~4.5 min parallel vs. ~7 min via orchestrator) and reduced main-session context growth. Counter-field races are a theoretical concern but did not cause data loss in this run. For higher confidence, use Mitigation B (skip shared-file updates in workers, do a single batch cleanup pass after).

---

## Known risk: shared file write conflicts

`wiki/index.md`, `wiki/log.md`, and venue pages are written by every agent. When 5 agents run in parallel, there is a risk that agents clobber each other's edits on these shared files. If this happens:

**Mitigation A (simplest):** Run agents sequentially (one at a time) instead of in parallel. Still saves orchestrator overhead (~130k tokens); loses parallelism speedup.

**Mitigation B:** Have each agent skip shared file updates (index, log, venue) and perform a single batch update pass in the main session after all paper pages are written.

Start with parallel execution and inspect the shared files after the run. If conflicts appear, switch to Mitigation A.

---

## Results: parallel direct subagents with Mitigation B (2026-05-29)

**Variant run:** 6 `speech-generation-ingest-agent` workers spawned simultaneously; each writes only `wiki/papers/{id}.md` and updates `raw/metadata/{id}.json`. All shared-file updates (index, log, 4 venue pages) done in a single main-session batch pass after all agents completed.

**Papers:** 2603.29339, 2508.11273, 2604.12438, 2604.01760, 2508.15442, 2025.acl-long.654 — 6/6 ingested, 0 failed.

**Token usage per worker:**

| Paper | Tokens | Tool uses | Wall time |
|-------|--------|-----------|-----------|
| 2603.29339 | 62,200 | 6 | ~92s |
| 2508.11273 | 34,880 | 9 | ~101s |
| 2604.12438 | 45,208 | 7 | ~98s |
| 2604.01760 | 47,622 | 8 | ~107s |
| 2508.15442 | 46,507 | 8 | ~92s |
| 2025.acl-long.654 | 44,233 | 7 | ~82s |
| **Total** | **280,650** | **45** | **~107s (parallel wall time)** |

**Token savings vs. parallel-without-mitigation (prior run):** 280,650 vs. 331,845 — **~15% reduction** (saved ~51k tokens). Savings come from agents not reading and editing the large shared files (index.md, log.md, venue pages).

**Shared-file conflicts:** Zero. All shared-file writes were done serially in the main session after all workers completed. No races, no lost rows, no stale counts.

**Batch cleanup overhead:** ~10 Edit calls in the main session, trivial token cost.

**Conclusion:** Mitigation B is the recommended approach. It is faster than all prior variants (~2 min wall time for 6 papers), eliminates write conflicts entirely, and reduces per-batch token cost by ~15% vs. parallel-without-mitigation. The batch cleanup pass is minimal and deterministic. **Adopt this as the standard parallel ingest workflow going forward.**
