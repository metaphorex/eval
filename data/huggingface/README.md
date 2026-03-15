# Metaphorex Dataset

A knowledge graph of conceptual metaphors, design patterns, archetypes, and cross-field mappings.

## Dataset Description

Each row is a **mapping** — a structured relationship between a source domain and a target domain.

### Columns

| Column | Type | Description |
|--------|------|-------------|
| `slug` | string | Unique kebab-case identifier |
| `name` | string | Human-readable name |
| `kind` | string | One of: conceptual-metaphor, design-pattern, archetype, paradigm, cross-field-mapping, dead-metaphor |
| `source_frame` | string | Source domain slug |
| `target_frame` | string | Target domain slug |
| `categories` | list[string] | Topic categories |
| `author` | string | Original author or agent identifier |
| `what_it_brings` | string | What the mapping illuminates |
| `where_it_breaks` | string | Where the mapping misleads or fails |
| `expressions` | string | Common linguistic expressions of this mapping |

### Usage

```python
from datasets import load_dataset

ds = load_dataset("metaphorex/metaphorex")
print(ds["train"][0])
```

### License

CC BY-SA 4.0

### Citation

```bibtex
@misc{metaphorex2026,
  title={Metaphorex: A Knowledge Graph of Conceptual Metaphors},
  url={https://github.com/metaphorex/metaphorex},
  year={2026}
}
```
