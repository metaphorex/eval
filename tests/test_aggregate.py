"""Tests for aggregation and reporting."""

import json
import tempfile
from pathlib import Path

from scoring.aggregate import ALL_CONDITIONS, build_comparison_table, group_results, load_results

SAMPLE_RESULTS = [
    {
        "scenario": "ml-training-pipeline",
        "condition": "baseline",
        "model": "nemotron-super",
        "response": "Some response text here",
        "scores": {"consistency_ratio": 0.8, "fidelity": 0.7, "mislead_quality": 0.6},
    },
    {
        "scenario": "ml-training-pipeline",
        "condition": "frames_only",
        "model": "nemotron-super",
        "response": "Frames only response",
        "scores": {"consistency_ratio": 0.9, "fidelity": 0.8, "mislead_quality": 0.7},
    },
    {
        "scenario": "ml-training-pipeline",
        "condition": "m4x_pairs",
        "model": "nemotron-super",
        "response": "Pairs response with context",
        "scores": {"consistency_ratio": 0.85, "fidelity": 0.75, "mislead_quality": 0.65},
    },
    {
        "scenario": "ml-training-pipeline",
        "condition": "baseline",
        "model": "qwen3.5-9b",
        "response": "Qwen response",
        "scores": None,
    },
]


def test_load_results():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(SAMPLE_RESULTS, f)
        f.flush()
        results = load_results([Path(f.name)])
    assert len(results) == 4


def test_group_results():
    grouped = group_results(SAMPLE_RESULTS)
    assert "ml-training-pipeline" in grouped
    assert "baseline" in grouped["ml-training-pipeline"]
    assert "nemotron-super" in grouped["ml-training-pipeline"]["baseline"]


def test_build_comparison_table():
    grouped = group_results(SAMPLE_RESULTS)
    table = build_comparison_table(grouped)
    assert len(table) == 2  # two models
    for row in table:
        assert "scenario" in row
        assert "model" in row


def test_build_comparison_table_includes_scores():
    grouped = group_results(SAMPLE_RESULTS)
    table = build_comparison_table(grouped)
    nemotron_row = [r for r in table if r["model"] == "nemotron-super"][0]
    assert nemotron_row["baseline_consistency"] == 0.8
    assert nemotron_row["baseline_fidelity"] == 0.7
    assert nemotron_row["frames_only_consistency"] == 0.9


def test_all_conditions_constant():
    assert ALL_CONDITIONS == ["baseline", "frames_only", "m4x_pairs", "m4x_full"]


def test_report_generation():
    from evals.naming.report import generate_report

    with tempfile.TemporaryDirectory() as tmpdir:
        output = Path(tmpdir) / "report.md"
        report = generate_report(SAMPLE_RESULTS, output)
        assert "# Naming Task Eval Results" in report
        assert output.exists()
        assert "ml-training-pipeline" in report
        assert "Baseline" in report
        assert "M4X Full" in report
