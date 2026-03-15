import pytest

from harnesses.in_context import CONDITIONS, SHARED_ENCOURAGEMENT, build_messages


def test_all_conditions_share_encouragement():
    """Every condition includes identical SHARED_ENCOURAGEMENT text."""
    system_desc = "Name 10 components of a distributed task queue."
    data_block = "- cooking\n- military\n- theater"

    texts = {}
    for cond in CONDITIONS:
        msgs = build_messages(system_desc, cond, data_block)
        texts[cond] = msgs[0]["content"]

    # All conditions must contain the shared encouragement (with system_desc filled in)
    encouragement = SHARED_ENCOURAGEMENT.format(system_desc=system_desc)
    for cond, text in texts.items():
        assert encouragement in text, f"{cond} missing shared encouragement"


def test_baseline_has_no_data_block():
    """Baseline condition should not include data preamble."""
    msgs = build_messages("Some system.", "baseline", "extra data here")
    assert "extra data here" not in msgs[0]["content"]
    assert "reference material" not in msgs[0]["content"]


def test_non_baseline_includes_data_block():
    """frames_only, m4x_pairs, m4x_full should include the data block."""
    data = "- cooking\n- military"
    for cond in ["frames_only", "m4x_pairs", "m4x_full"]:
        msgs = build_messages("Some system.", cond, data)
        assert data in msgs[0]["content"], f"{cond} missing data block"
        assert "reference material" in msgs[0]["content"]


def test_encouragement_no_knowledge_graph_mention():
    """Shared encouragement must not mention 'knowledge graph' or 'catalog'."""
    assert "knowledge graph" not in SHARED_ENCOURAGEMENT.lower()
    assert "catalog" not in SHARED_ENCOURAGEMENT.lower()


def test_unknown_condition_raises():
    """Unknown condition should raise ValueError."""
    with pytest.raises(ValueError, match="Unknown condition"):
        build_messages("desc", "unknown", "")


def test_conditions_list():
    """CONDITIONS should have exactly 4 entries."""
    assert CONDITIONS == ["baseline", "frames_only", "m4x_pairs", "m4x_full"]
