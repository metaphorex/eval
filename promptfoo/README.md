# Prompt Sensitivity Testing with promptfoo

Tests whether minor prompt wording changes affect eval results.

## Setup

```bash
# No install needed — runs via npx
npx promptfoo@latest eval --config promptfoo/promptfooconfig.yaml
```

## View results

```bash
npx promptfoo@latest view
```

## What it tests

3 prompt variants × 2 cheap models × 2 scenarios = 12 runs.

- **v1.txt**: Primary wording (uses "metaphorical frame")
- **v2.txt**: Alternative word choice (uses "metaphorical domain")
- **v3.txt**: Different instruction ordering (encouragement after system desc)

## Environment

Set `OPENROUTER_API_KEY` in your environment. promptfoo uses the OpenRouter
provider prefix (`openrouter:model-id`).

## Interpreting results

Look for:
- **Format compliance**: Do all variants produce pipe-separated numbered lists?
- **Frame consistency**: Do all variants produce names from a single domain?
- **Stability**: Do results vary significantly across wording?

If results are stable across v1/v2/v3, the wording doesn't matter much.
If they diverge, pick the most consistent variant for the real eval.
