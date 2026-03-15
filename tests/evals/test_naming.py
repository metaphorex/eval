from evals.naming.task import SCENARIOS, NamingScenario
from evals.naming.run import run_single


def test_scenarios_have_required_fields():
    assert len(SCENARIOS) >= 3
    for s in SCENARIOS:
        assert isinstance(s, NamingScenario)
        assert s.system_desc
        assert s.expected_component_count == 10


def test_run_single_baseline_dry_run():
    data_blocks = {"baseline": "", "frames_only": "frames", "m4x_pairs": "pairs", "m4x_full": "full"}
    result = run_single(SCENARIOS[0], "baseline", "nemotron-super", data_blocks, dry_run=True)
    assert result["response"] == "[DRY RUN]"
    assert result["scenario"] == "ml-training-pipeline"
    assert result["condition"] == "baseline"


def test_run_single_frames_only_dry_run():
    data_blocks = {"baseline": "", "frames_only": "- cooking\n- military", "m4x_pairs": "pairs", "m4x_full": "full"}
    result = run_single(SCENARIOS[0], "frames_only", "nemotron-super", data_blocks, dry_run=True)
    assert result["response"] == "[DRY RUN]"
    assert result["condition"] == "frames_only"


def test_run_single_m4x_pairs_dry_run():
    data_blocks = {"baseline": "", "frames_only": "frames", "m4x_pairs": "pairs ctx", "m4x_full": "full"}
    result = run_single(SCENARIOS[0], "m4x_pairs", "nemotron-super", data_blocks, dry_run=True)
    assert result["response"] == "[DRY RUN]"
    assert result["condition"] == "m4x_pairs"


def test_run_single_m4x_full_dry_run():
    data_blocks = {"baseline": "", "frames_only": "frames", "m4x_pairs": "pairs", "m4x_full": "full ctx"}
    result = run_single(SCENARIOS[0], "m4x_full", "nemotron-super", data_blocks, dry_run=True)
    assert result["response"] == "[DRY RUN]"
    assert result["condition"] == "m4x_full"


def test_all_four_conditions_dry_run():
    """All 4 conditions should work in dry-run mode."""
    from harnesses.in_context import CONDITIONS

    data_blocks = {"baseline": "", "frames_only": "frames", "m4x_pairs": "pairs", "m4x_full": "full"}
    for condition in CONDITIONS:
        result = run_single(SCENARIOS[0], condition, "nemotron-super", data_blocks, dry_run=True)
        assert result["response"] == "[DRY RUN]"
        assert result["condition"] == condition
