"""Load and query m4x data snapshots."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

SNAPSHOTS_DIR = Path("data/snapshots")


def load_snapshot(path: Path) -> list[dict]:
    """Load a JSON snapshot produced by metaphorex validate.py extract."""
    with open(path) as f:
        return json.load(f)


def create_snapshot(metaphorex_repo: Path, output: Path) -> Path:
    """Run validate.py extract against a metaphorex repo and save snapshot."""
    result = subprocess.run(
        ["uv", "run", "scripts/validate.py", "extract"],
        cwd=metaphorex_repo, capture_output=True, text=True, check=True,
    )
    output.write_text(result.stdout)
    return output


def fetch_snapshot(
    version: str | None = None,
    repo: str = "metaphorex/metaphorex",
) -> Path:
    """Download a snapshot from a GitHub Release.

    Args:
        version: CalVer tag (e.g. '2026.03.14'). None = latest release.
        repo: GitHub repo in 'owner/name' format.

    Returns:
        Path to the downloaded snapshot JSON file.
    """
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    if version is None:
        # Fetch latest release tag
        result = subprocess.run(
            ["gh", "release", "view", "--repo", repo, "--json", "tagName", "-q", ".tagName"],
            capture_output=True, text=True, check=True,
        )
        version = result.stdout.strip()

    # Check if already downloaded
    pattern = f"metaphorex-{version}.json"
    target = SNAPSHOTS_DIR / pattern
    if target.exists():
        return target

    # Download from release
    subprocess.run(
        [
            "gh", "release", "download", version,
            "--repo", repo,
            "--pattern", "metaphorex-*.json",
            "--dir", str(SNAPSHOTS_DIR),
        ],
        check=True,
    )

    # Find the downloaded file
    matches = list(SNAPSHOTS_DIR.glob(f"metaphorex-{version}*.json"))
    if not matches:
        raise FileNotFoundError(f"No snapshot file found after downloading release {version}")
    return matches[0]
