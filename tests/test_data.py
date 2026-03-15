from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures"


def test_load_snapshot_parses_mappings():
    from data.snapshot import load_snapshot

    mappings = load_snapshot(FIXTURES / "snapshot_sample.json")
    assert len(mappings) == 5
    assert all("slug" in m for m in mappings)
    assert all("source_frame" in m for m in mappings)
    assert all("sections" in m for m in mappings)


def test_to_pairs_extracts_fields():
    from data.snapshot import load_snapshot
    from data.transform import to_pairs

    mappings = load_snapshot(FIXTURES / "snapshot_sample.json")
    pairs = to_pairs(mappings)
    assert len(pairs) == len(mappings)
    for p in pairs:
        assert "source_frame" in p
        assert "target_frame" in p
        assert "expressions" in p
        assert "where_it_breaks" in p
        assert "slug" in p


def test_to_context_block_contains_all_mappings():
    from data.snapshot import load_snapshot
    from data.transform import to_context_block

    mappings = load_snapshot(FIXTURES / "snapshot_sample.json")
    block = to_context_block(mappings)
    for m in mappings:
        assert m["name"] in block
    assert "What It Brings" in block
    assert "Where It Breaks" in block


def test_to_frames_list():
    from data.snapshot import load_snapshot
    from data.transform import to_frames_list

    mappings = load_snapshot(FIXTURES / "snapshot_sample.json")
    frames = to_frames_list(mappings)
    # Should be a bullet list of unique source frames
    lines = frames.strip().split("\n")
    assert all(line.startswith("- ") for line in lines)
    # Fixture has these source frames
    unique_frames = {m["source_frame"] for m in mappings}
    assert len(lines) == len(unique_frames)
    for frame in unique_frames:
        assert f"- {frame}" in frames


def test_to_pairs_block():
    from data.snapshot import load_snapshot
    from data.transform import to_pairs_block

    mappings = load_snapshot(FIXTURES / "snapshot_sample.json")
    block = to_pairs_block(mappings)
    for m in mappings:
        assert m["name"] in block
        assert m["source_frame"] in block
        assert m["target_frame"] in block
    # Each line is a bullet
    lines = [line for line in block.strip().split("\n") if line.strip()]
    assert len(lines) == len(mappings)
