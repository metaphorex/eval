"""Tests for snapshot fetching from GitHub releases."""

import json
from unittest.mock import MagicMock, patch

from data.snapshot import fetch_snapshot


def test_fetch_snapshot_with_version(tmp_path):
    """fetch_snapshot with explicit version calls gh release download."""
    snapshots_dir = tmp_path / "snapshots"

    # Create a fake downloaded file
    def fake_download(*args, **kwargs):
        snapshots_dir.mkdir(parents=True, exist_ok=True)
        snapshot = [{"slug": "test", "name": "Test"}]
        (snapshots_dir / "metaphorex-2026.03.14.json").write_text(json.dumps(snapshot))

    with patch("data.snapshot.SNAPSHOTS_DIR", snapshots_dir), \
         patch("subprocess.run") as mock_run:
        mock_run.side_effect = fake_download
        path = fetch_snapshot(version="2026.03.14")
        assert path.exists()
        assert "2026.03.14" in path.name


def test_fetch_snapshot_returns_cached(tmp_path):
    """If snapshot already exists locally, don't download again."""
    snapshots_dir = tmp_path / "snapshots"
    snapshots_dir.mkdir(parents=True, exist_ok=True)
    cached = snapshots_dir / "metaphorex-2026.03.14.json"
    cached.write_text('[{"slug": "cached"}]')

    with patch("data.snapshot.SNAPSHOTS_DIR", snapshots_dir):
        path = fetch_snapshot(version="2026.03.14")
        assert path == cached


def test_fetch_snapshot_latest(tmp_path):
    """fetch_snapshot without version queries latest release."""
    snapshots_dir = tmp_path / "snapshots"

    call_count = 0

    def fake_run(cmd, **kwargs):
        nonlocal call_count
        call_count += 1
        mock = MagicMock()
        mock.returncode = 0
        if call_count == 1:
            # First call: gh release view to get tag
            mock.stdout = "2026.03.14\n"
        else:
            # Second call: gh release download
            snapshots_dir.mkdir(parents=True, exist_ok=True)
            (snapshots_dir / "metaphorex-2026.03.14.json").write_text('[{"slug": "latest"}]')
        return mock

    with patch("data.snapshot.SNAPSHOTS_DIR", snapshots_dir), \
         patch("subprocess.run", side_effect=fake_run):
        path = fetch_snapshot(version=None)
        assert path.exists()
