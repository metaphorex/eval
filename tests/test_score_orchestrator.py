"""Tests for the scoring orchestrator."""

from scoring.score import score_results, SCENARIO_DESCS


SAMPLE_RESULTS = [
    {
        "scenario": "ml-training-pipeline",
        "condition": "baseline",
        "model": "nemotron-super",
        "response": "[DRY RUN]",
    },
    {
        "scenario": "ml-training-pipeline",
        "condition": "m4x_full",
        "model": "nemotron-super",
        "response": "1. Head Chef | Job Submission | ...",
    },
]


def test_score_results_dry_run():
    """Dry-run mode sets all scores to None."""
    scored = score_results(SAMPLE_RESULTS, dry_run=True)
    assert len(scored) == len(SAMPLE_RESULTS)
    for r in scored:
        assert r["scores"] is None


def test_score_results_skips_dry_run_responses():
    """Results with '[DRY RUN]' response always get scores=None."""
    scored = score_results(SAMPLE_RESULTS, dry_run=True)
    assert scored[0]["scores"] is None
    assert scored[0]["response"] == "[DRY RUN]"


def test_score_results_preserves_original_fields():
    """Scoring should preserve all original result fields."""
    scored = score_results(SAMPLE_RESULTS, dry_run=True)
    for orig, s in zip(SAMPLE_RESULTS, scored):
        assert s["scenario"] == orig["scenario"]
        assert s["condition"] == orig["condition"]
        assert s["model"] == orig["model"]
        assert s["response"] == orig["response"]


def test_scenario_descs_cover_all_scenarios():
    """All known scenarios must have descriptions for scoring."""
    from evals.naming.task import SCENARIOS

    for s in SCENARIOS:
        assert s.name in SCENARIO_DESCS, f"Missing scenario desc: {s.name}"
