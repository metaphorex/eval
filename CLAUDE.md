# Metaphorex Eval

Evaluation harnesses measuring whether the Metaphorex knowledge graph
improves LLM performance on naming, reasoning, and metaphor detection tasks.

## API Provider

**OpenRouter only.** All LLM calls — eval runs AND scoring — go through
OpenRouter (`https://openrouter.ai/api/v1`). The only API key needed is
`OPENROUTER_API_KEY`. There is no Anthropic SDK dependency. Do not add one.

Set the key in `.envrc` (gitignored):
```bash
export OPENROUTER_API_KEY=sk-or-v1-...
```

## Build & Test

```bash
uv sync --dev
uv run ruff check .
uv run pytest tests/ -v
```

Zero warnings, zero errors is the precedent.

## Running Evals

```bash
source .envrc

# 1. Run (60 API calls, ~2 min)
uv run python -m evals.naming.run --snapshot-version 2026.03.14

# 2. Score (~120 API calls via OpenRouter)
uv run python -m scoring.score --results results/naming/run-*.json

# 3. Report
uv run python -m evals.naming.report --results results/scored/scored-*.json --output results/naming/report.md
```

## Directory Structure

```
evals/naming/        # Naming task: scenarios, runner, report
harnesses/           # Prompt templates (shared encouragement, data preamble)
scoring/             # LLM-as-judge scorers + orchestrator (all via OpenRouter)
data/                # Snapshot loading, transforms, HuggingFace push
promptfoo/           # Prompt sensitivity testing config
results/             # Raw runs + scored results
tests/               # 40 tests, all fixture-based, no API keys needed
```

## Key Conventions

- Content repo releases CalVer snapshots (`2026.03.14`); this repo fetches them
- 4 eval conditions: baseline, frames_only, m4x_pairs, m4x_full (capped at 50 entries)
- Scoring uses `google/gemini-2.5-flash-lite` via OpenRouter (cheap, fast)
- `m4x_full` is capped at 50 mappings to stay under model context limits
