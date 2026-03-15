"""Tests for HuggingFace dataset push (no actual pushing)."""

from pathlib import Path

from data.huggingface.push import snapshot_to_rows
from data.snapshot import load_snapshot

FIXTURES = Path(__file__).parent / "fixtures"


def test_snapshot_to_rows_structure():
    """Verify row structure matches expected HF columns."""
    mappings = load_snapshot(FIXTURES / "snapshot_sample.json")
    rows = snapshot_to_rows(mappings)
    assert len(rows) == len(mappings)

    expected_columns = {
        "slug", "name", "kind", "source_frame", "target_frame",
        "categories", "author", "what_it_brings", "where_it_breaks", "expressions",
    }
    for row in rows:
        assert set(row.keys()) == expected_columns


def test_snapshot_to_rows_content():
    """Verify row content is extracted correctly."""
    mappings = load_snapshot(FIXTURES / "snapshot_sample.json")
    rows = snapshot_to_rows(mappings)

    first = rows[0]
    assert first["slug"] == mappings[0]["slug"]
    assert first["name"] == mappings[0]["name"]
    assert first["kind"] == mappings[0]["kind"]
    assert first["source_frame"] == mappings[0]["source_frame"]
    assert first["target_frame"] == mappings[0]["target_frame"]
    assert first["what_it_brings"]  # should be non-empty
    assert first["where_it_breaks"]  # should be non-empty
    assert first["expressions"]  # should be non-empty


def test_snapshot_to_rows_categories_are_lists():
    """Categories should remain as lists."""
    mappings = load_snapshot(FIXTURES / "snapshot_sample.json")
    rows = snapshot_to_rows(mappings)
    for row in rows:
        assert isinstance(row["categories"], list)
