# Metaphorex Eval

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Does a knowledge graph of metaphors help LLMs reason better? We're testing it.**

[Metaphorex](https://github.com/metaphorex/metaphorex) is a knowledge graph of 400+ conceptual metaphors, design patterns, and archetypes -- each with structured "Where It Breaks" analysis. This repo contains evaluation harnesses that measure whether that data actually improves LLM performance.

## Current Status: Pivoting to Tool Use

The first experiment (naming task) tested whether naively dumping catalog data into a prompt improves LLM output. **It doesn't.** See [results/naming/RESULTS.md](results/naming/RESULTS.md) for details.

Models already know how to pick a metaphorical frame and name things consistently. Giving them a raw dump of 400+ mappings adds noise without improving fidelity or mislead quality. The naming task was a hasty spot-check -- useful for proving the pipeline works, but the wrong test for the catalog's actual value.

**Next direction: tool use.** The catalog's value isn't in bulk context injection -- it's in narrow, targeted retrieval. Think: "find me a metaphor whose source domain maps structurally to this system" or "what does this metaphor hide?" The next round of work focuses on building useful search and identification tools (MCP/function-calling), then evaluating whether those tools improve specific reasoning tasks.

## Hypotheses

1. ~~**Naming consistency.** LLMs with m4x data produce more consistent, structurally faithful names for system components.~~ (Not supported -- see results)
2. **Failure-mode detection.** LLMs with "Where It Breaks" data identify more failure modes in metaphor-framed systems.
3. **Metaphor detection.** LLMs with m4x data detect conceptual metaphors in text with higher precision and recall.

## Repo Structure

```
evals/              # Eval definitions (prompts, schemas, expected outputs)
  naming/           # First eval: component naming task (on ice)
harnesses/          # Prompt templates for in-context conditions
scoring/            # LLM-as-judge scorers (all via OpenRouter)
data/
  snapshots/        # Point-in-time exports of m4x catalog (generated)
  huggingface/      # HuggingFace dataset artifacts
promptfoo/          # Prompt sensitivity testing config
results/
  naming/           # Naming task results and analysis
  scored/           # Scored results
tests/              # 40 tests, fixture-based, no API keys needed
```

## Quick Start

```bash
uv sync --dev
uv run pytest
```

## Related

- [Metaphorex](https://github.com/metaphorex/metaphorex) -- the knowledge graph
- [metaphorex.org](https://metaphorex.org) -- the site

## License

MIT
