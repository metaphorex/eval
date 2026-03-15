"""Aggregate eval results for comparison and reporting."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ALL_CONDITIONS = ["baseline", "frames_only", "m4x_pairs", "m4x_full"]


def load_results(paths: list[Path]) -> list[dict]:
    """Load and merge results from multiple run files."""
    results = []
    for p in paths:
        with open(p) as f:
            results.extend(json.load(f))
    return results


def group_results(results: list[dict]) -> dict:
    """Group results by scenario -> condition -> model.

    Returns nested dict: {scenario: {condition: {model: result_dict}}}
    """
    grouped: dict = defaultdict(lambda: defaultdict(dict))
    for r in results:
        grouped[r["scenario"]][r["condition"]][r["model"]] = r
    return dict(grouped)


def build_comparison_table(grouped: dict) -> list[dict]:
    """Build a flat comparison table for display.

    Each row includes response lengths and scores (if available) for all 4 conditions.
    """
    rows = []
    for scenario, conditions in sorted(grouped.items()):
        models: set[str] = set()
        for cond_data in conditions.values():
            models.update(cond_data.keys())

        for model in sorted(models):
            row: dict = {"scenario": scenario, "model": model}
            for condition in ALL_CONDITIONS:
                if condition in conditions and model in conditions[condition]:
                    entry = conditions[condition][model]
                    resp = entry.get("response", "")
                    row[f"{condition}_len"] = len(resp) if resp else 0
                    row[f"{condition}_has_response"] = resp != "[DRY RUN]" and bool(resp)

                    # Include scores if available
                    scores = entry.get("scores")
                    if scores:
                        row[f"{condition}_consistency"] = scores.get("consistency_ratio")
                        row[f"{condition}_fidelity"] = scores.get("fidelity")
                        row[f"{condition}_mislead"] = scores.get("mislead_quality")
                else:
                    row[f"{condition}_len"] = None
                    row[f"{condition}_has_response"] = False
            rows.append(row)
    return rows
