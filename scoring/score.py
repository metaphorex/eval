"""Scoring orchestrator: read raw results, call scorers, write scored output.

Usage:
    uv run python -m scoring.score --results results/naming/run-*.json
    uv run python -m scoring.score --results results/naming/run-*.json --dry-run
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from scoring.aggregate import load_results
from scoring.frame_consistency import score_frame_consistency
from scoring.structural_fidelity import score_structural_fidelity

# Map scenario names to system descriptions
SCENARIO_DESCS = {
    "ml-training-pipeline": (
        "A distributed task queue for ML model training jobs. Components include: "
        "job submission, resource allocation, data loading, model checkpointing, "
        "gradient synchronization, failure recovery, result aggregation, scheduling, "
        "monitoring, and artifact storage."
    ),
    "content-moderation-system": (
        "An automated content moderation pipeline for a social platform. Components include: "
        "content ingestion, classification, human review queue, appeal handling, policy enforcement, "
        "audit logging, reporter feedback, false positive tracking, escalation routing, and metrics dashboard."
    ),
    "supply-chain-tracker": (
        "A real-time supply chain visibility platform. Components include: "
        "shipment tracking, inventory sync, supplier onboarding, demand forecasting, "
        "exception alerting, customs documentation, carrier integration, warehouse coordination, "
        "returns processing, and compliance reporting."
    ),
}

SCORED_DIR = Path("results/scored")


def score_results(results: list[dict], dry_run: bool = False) -> list[dict]:
    """Score all non-dry-run results.

    Args:
        results: Raw result dicts from the naming eval runner.
        dry_run: If True, skip API calls and set scores to None.

    Returns:
        Same results with added 'scores' dict.
    """
    client = None
    if not dry_run:
        from scoring.client import make_scoring_client

        client = make_scoring_client()

    scored = []
    for r in results:
        result = dict(r)
        response = r.get("response", "")

        if response == "[DRY RUN]" or not response or dry_run:
            result["scores"] = None
            scored.append(result)
            continue

        system_desc = SCENARIO_DESCS.get(r["scenario"], "")

        consistency = score_frame_consistency(response, client=client)
        fidelity_result = score_structural_fidelity(response, system_desc, client=client)

        result["scores"] = {
            "consistency_ratio": consistency,
            "fidelity": fidelity_result["fidelity"],
            "mislead_quality": fidelity_result["mislead_quality"],
        }
        scored.append(result)

    return scored


def main():
    parser = argparse.ArgumentParser(description="Score naming eval results")
    parser.add_argument(
        "--results",
        nargs="+",
        type=Path,
        required=True,
        help="Raw result JSON files to score",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip API calls, write scores as null",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output path (default: results/scored/scored-TIMESTAMP.json)",
    )
    args = parser.parse_args()

    results = load_results(args.results)
    print(f"Loaded {len(results)} results from {len(args.results)} file(s)")

    scoreable = [r for r in results if r.get("response") != "[DRY RUN]" and r.get("response")]
    print(f"Scoring {len(scoreable)} responses (skipping {len(results) - len(scoreable)} dry-run/empty)")

    scored = score_results(results, dry_run=args.dry_run)

    SCORED_DIR.mkdir(parents=True, exist_ok=True)
    if args.output:
        out = args.output
    else:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        out = SCORED_DIR / f"scored-{timestamp}.json"

    out.write_text(json.dumps(scored, indent=2))
    print(f"Scored results saved to {out}")


if __name__ == "__main__":
    main()
