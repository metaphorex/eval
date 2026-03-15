"""Push metaphorex snapshot to HuggingFace as a dataset.

Usage:
    uv run python -m data.huggingface.push --snapshot data/snapshots/metaphorex-2026.03.14.json
    uv run python -m data.huggingface.push --snapshot-version 2026.03.14
    uv run python -m data.huggingface.push --snapshot tests/fixtures/snapshot_sample.json --dry-run
"""

from __future__ import annotations

import argparse
from pathlib import Path


def snapshot_to_rows(mappings: list[dict]) -> list[dict]:
    """Convert snapshot mappings to flat HuggingFace dataset rows."""
    rows = []
    for m in mappings:
        sections = m.get("sections", {})
        rows.append({
            "slug": m["slug"],
            "name": m["name"],
            "kind": m["kind"],
            "source_frame": m["source_frame"],
            "target_frame": m["target_frame"],
            "categories": m.get("categories", []),
            "author": m.get("author", ""),
            "what_it_brings": sections.get("What It Brings", ""),
            "where_it_breaks": sections.get("Where It Breaks", ""),
            "expressions": sections.get("Expressions", ""),
        })
    return rows


def main():
    parser = argparse.ArgumentParser(description="Push metaphorex snapshot to HuggingFace")
    snapshot_group = parser.add_mutually_exclusive_group(required=True)
    snapshot_group.add_argument("--snapshot", type=Path, help="Path to snapshot JSON")
    snapshot_group.add_argument("--snapshot-version", type=str, help="CalVer version to fetch")
    parser.add_argument("--repo-id", type=str, default="metaphorex/metaphorex", help="HuggingFace repo ID")
    parser.add_argument("--dry-run", action="store_true", help="Print dataset summary without pushing")
    args = parser.parse_args()

    if args.snapshot_version:
        from data.snapshot import fetch_snapshot

        snapshot_path = fetch_snapshot(version=args.snapshot_version)
    else:
        snapshot_path = args.snapshot

    from data.snapshot import load_snapshot

    mappings = load_snapshot(snapshot_path)
    rows = snapshot_to_rows(mappings)

    print(f"Dataset: {len(rows)} mappings")
    print(f"Columns: {list(rows[0].keys()) if rows else '(empty)'}")
    print(f"Kinds: {sorted(set(r['kind'] for r in rows))}")
    print(f"Source frames: {len(set(r['source_frame'] for r in rows))} unique")
    print(f"Target frames: {len(set(r['target_frame'] for r in rows))} unique")

    if args.dry_run:
        print("\n[DRY RUN] Would push to HuggingFace. Sample row:")
        if rows:
            sample = rows[0]
            for k, v in sample.items():
                val = str(v)[:80] + "..." if len(str(v)) > 80 else str(v)
                print(f"  {k}: {val}")
        return

    from datasets import Dataset

    ds = Dataset.from_list(rows)
    print(f"\nPushing to {args.repo_id}...")
    ds.push_to_hub(args.repo_id, private=False)
    print("Done!")


if __name__ == "__main__":
    main()
