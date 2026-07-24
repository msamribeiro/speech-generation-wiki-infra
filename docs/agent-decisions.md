# Shared Agent Decisions

This tracked file records durable decisions needed by both Claude Code and Codex. It is curated
project knowledge, not an automatic memory dump. Current schemas, `STATUS.md`, `BACKLOG.md`, and
the operational logs remain authoritative for live state.

## 2026-07-20 — Claude/Codex interoperability

- `AGENTS.md` is the model-neutral operating contract; `CLAUDE.md` imports it.
- Canonical pipeline workflows live as repository skills in `.agents/skills/`. Claude subagents
  are thin adapters that preload those skills through the `.claude/skills` symlink.
- The pipeline is Fetch → Filter → Parse → Ingest → Integrate → Render. Integration writes
  `wiki/_claims/`; rendering derives human-facing Markdown from those YAML files. The original
  dossier output named here was superseded by the 2026-07-24 two-depth decision below.
- The conservative renderer formerly called v2 is canonical under the stable
  `speech-generation-render-agent` name.
- Wiki writes go to the sibling `speech-generation-wiki-content` clone, resolved by
  `scripts/resolve_wiki_dir.py`; the infra `wiki/` submodule is not a write target.
- Private Claude or Codex memory is never a source of truth. Verify useful discoveries and record
  them in the appropriate tracked documentation, status, backlog, log, or dated record.

## 2026-07-24 — Two concept rendering depths

- Each `wiki/_claims/{slug}.yaml` file has two human-facing renderings under `wiki/concepts/`:
  **Overview** for rapid state-of-the-art scanning and **In Depth** for detailed research synthesis.
- Both formats are projections of the same concept-level data and are produced from one shared
  editorial plan so their assessments remain consistent.
- The claim YAML remains the exhaustive machine-readable layer. Future Markdown renders do not
  reproduce the full claim graph or paper inventory.
- The former Evidence Dossier format is legacy. The new formats were prototyped for
  `speech-to-speech`, `evaluation-metrics`, `flow-matching`, and `rlhf-speech`, then promoted to
  canonical content pages on 2026-07-24 after review found no blockers. The production
  specification is `docs/design/concept-rendering.md`. The obsolete `wiki/evidence/` directory was
  removed after all five integrated concepts had Overview and In Depth renderings.

## 2026-07-20 — Cross-runtime generation provenance

- Future generated or substantively regenerated content pages use generation schema version 2.
- Provenance records `runtime` (`claude-code` or `codex`), `provider` (`anthropic` or `openai`),
  exact model ID, stable logical agent, date, and infra commit.
- Existing provenance blocks without `schema_version` remain valid historical version-1 records;
  they are upgraded when their page is next regenerated rather than through a bulk rewrite.
- Agent-operation changelog entries include runtime, provider, and model even when the operation
  updates a non-page artifact such as claim YAML.
