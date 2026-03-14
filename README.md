# Metaphorex Eval

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Does a knowledge graph of metaphors help LLMs reason better? We're testing it.**

[Metaphorex](https://github.com/metaphorex/metaphorex) is a knowledge graph of 400+ conceptual metaphors, design patterns, and archetypes -- each with structured "Where It Breaks" analysis. This repo contains evaluation harnesses that measure whether that data actually improves LLM performance.

## Hypotheses

1. **Naming consistency.** LLMs with m4x data produce more consistent, structurally faithful names for system components.
2. **Failure-mode detection.** LLMs with "Where It Breaks" data identify more failure modes in metaphor-framed systems.
3. **Metaphor detection.** LLMs with m4x data detect conceptual metaphors in text with higher precision and recall.

## Current Status

Setting up. First experiment: the naming task.

## Repo Structure

```
evals/              # Eval definitions (prompts, schemas, expected outputs)
  naming/           # First eval: component naming task
harnesses/          # Runners that call LLM APIs and collect responses
scoring/            # Scoring functions (consistency, faithfulness, etc.)
data/
  snapshots/        # Point-in-time exports of m4x catalog (generated)
  huggingface/      # HuggingFace dataset artifacts
results/
  scored/           # Scored results (committed)
  raw/              # Raw API responses (gitignored)
tests/              # Unit and eval tests
```

## Quick Start

```bash
uv sync --dev
uv run pytest
```

## Contributing

We're building in public. Issues and PRs welcome.

## Related

- [Metaphorex](https://github.com/metaphorex/metaphorex) -- the knowledge graph
- [metaphorex.org](https://metaphorex.org) -- the site

## License

MIT
