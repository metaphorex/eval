# Naming Task Results — 2026-03-15

## TL;DR

Dumping m4x catalog data into the prompt does not improve LLM naming performance.
Baseline (no data) matches or beats all data-augmented conditions. This experiment
is **abandoned** — the catalog's value is not in bulk context injection.

## Setup

- **4 conditions:** baseline (no data), frames_only (~20 source domain names),
  m4x_pairs (compact name + source→target for all 431), m4x_full (first 50
  mappings with full What It Brings / Where It Breaks / Expressions)
- **3 scenarios:** ml-training-pipeline, content-moderation-system, supply-chain-tracker
- **5 models:** deepseek-v3, gemini-flash-lite, gemma-3-27b, gpt5-nano, qwen3.5-9b
- **Scoring:** LLM-as-judge (gemini-flash-lite via OpenRouter) for frame consistency,
  structural fidelity, and mislead quality
- gpt5-nano and qwen3.5-9b returned dry-run results (not scored)

## Results

| Scenario | Model | Baseline | Frames Only | M4X Pairs | M4X Full |
|----------|-------|----------|-------------|-----------|----------|
| content-moderation-system | deepseek-v3 | C:1.00 F:0.77 M:0.61 | C:1.00 F:0.76 M:0.66 | C:0.90 F:0.76 M:0.71 | C:1.00 F:0.71 M:0.71 |
| content-moderation-system | gemini-flash-lite | C:1.00 F:0.73 M:0.70 | C:0.60 F:0.69 M:0.72 | C:1.00 F:0.72 M:0.69 | C:1.00 F:0.65 M:0.71 |
| content-moderation-system | gemma-3-27b | C:1.00 F:0.67 M:0.65 | C:1.00 F:0.60 M:0.75 | C:1.00 F:0.71 M:0.80 | C:1.00 F:0.67 M:0.71 |
| ml-training-pipeline | deepseek-v3 | C:1.00 F:0.78 M:0.78 | C:1.00 F:0.71 M:0.80 | C:1.00 F:0.73 M:0.79 | C:1.00 F:0.59 M:0.76 |
| ml-training-pipeline | gemini-flash-lite | C:1.00 F:0.68 M:0.77 | C:1.00 F:0.72 M:0.71 | C:1.00 F:0.69 M:0.73 | C:1.00 F:0.61 M:0.72 |
| ml-training-pipeline | gemma-3-27b | C:1.00 F:0.77 M:0.73 | C:1.00 F:0.77 M:0.63 | C:1.00 F:0.65 M:0.64 | C:1.00 F:0.68 M:0.75 |
| supply-chain-tracker | deepseek-v3 | C:1.00 F:0.73 M:0.78 | C:1.00 F:0.67 M:0.70 | C:0.80 F:0.76 M:0.72 | C:1.00 F:0.75 M:0.79 |
| supply-chain-tracker | gemini-flash-lite | C:1.00 F:0.75 M:0.72 | C:0.40 F:0.73 M:0.73 | C:1.00 F:0.64 M:0.75 | C:1.00 F:0.79 M:0.77 |
| supply-chain-tracker | gemma-3-27b | C:1.00 F:0.67 M:0.70 | C:1.00 F:0.68 M:0.75 | C:1.00 F:0.69 M:0.71 | C:1.00 F:0.75 M:0.71 |

**Score legend:** C = frame consistency (0–1), F = structural fidelity (0–1), M = mislead quality (0–1)

## Averages across 9 scored cells

| Condition | Consistency | Fidelity | Mislead |
|-----------|------------|----------|---------|
| Baseline | **1.00** | **0.73** | 0.72 |
| Frames Only | 0.89 | 0.70 | 0.72 |
| M4X Pairs | 0.97 | 0.71 | 0.73 |
| M4X Full | 1.00 | 0.69 | 0.74 |

## Interpretation

- **Consistency:** Baseline is perfect. Adding frame lists actually *hurts* —
  gemini-flash-lite gets distracted and picks from multiple domains.
- **Fidelity:** Baseline wins. More data → slightly worse name-role mapping.
- **Mislead quality:** Flat across conditions. "Where It Breaks" content gives
  a negligible +0.02 bump, not meaningful at this sample size.

## Why this doesn't mean the catalog is useless

1. **Wrong task.** "Name 10 things from one metaphor" is easy. Models do it cold.
   The catalog's value is in tasks models *can't* do without it: identifying which
   metaphor is operating in existing code, surfacing non-obvious failure modes,
   or finding structural analogues across domains.
2. **Wrong delivery.** Dumping 400 mappings into a prompt is not how anyone would
   use this data. The real use case is targeted retrieval: "find me metaphors whose
   source domain is X" or "what breaks when you use Y metaphor for Z?"
3. **Weak judge.** gemini-flash-lite scoring gemini-flash-lite is circular. The
   0.59–0.80 score range is suspiciously narrow — likely judge insensitivity.
4. **N=1 per cell, 40% of models missing.** Not enough data to draw conclusions
   even if the task were right.

## Next steps

Abandon this approach. Focus on tool-use evals: build MCP tools for targeted
metaphor search and identification, then measure whether those tools improve
specific reasoning tasks where models actually need help.
