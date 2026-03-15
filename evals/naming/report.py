"""Generate a markdown report from naming task eval results."""

from __future__ import annotations

import argparse
from pathlib import Path

from scoring.aggregate import ALL_CONDITIONS, build_comparison_table, group_results, load_results


def _score_cell(row: dict, condition: str) -> str:
    """Format a score cell for the summary table."""
    has = row.get(f"{condition}_has_response", False)
    if not has:
        if row.get(f"{condition}_len") is not None:
            return "dry run"
        return "—"

    consistency = row.get(f"{condition}_consistency")
    fidelity = row.get(f"{condition}_fidelity")
    mislead = row.get(f"{condition}_mislead")

    if consistency is not None:
        return f"C:{consistency:.2f} F:{fidelity:.2f} M:{mislead:.2f}"

    # Fallback: show response length if no scores
    length = row.get(f"{condition}_len", 0)
    return f"({length} chars)"


def generate_report(results: list[dict], output: Path, include_responses: bool = False) -> str:
    """Generate a markdown report from eval results."""
    grouped = group_results(results)
    table = build_comparison_table(grouped)

    condition_headers = {
        "baseline": "Baseline",
        "frames_only": "Frames Only",
        "m4x_pairs": "M4X Pairs",
        "m4x_full": "M4X Full",
    }

    header_row = "| Scenario | Model | " + " | ".join(condition_headers[c] for c in ALL_CONDITIONS) + " |"
    sep_row = "|----------|-------|" + "|".join("-" * max(len(condition_headers[c]), 10) for c in ALL_CONDITIONS) + "|"

    lines = [
        "# Naming Task Eval Results",
        "",
        f"**Total runs:** {len(results)}",
        "",
        "**Score legend:** C = frame consistency, F = fidelity, M = mislead quality (all 0.0–1.0)",
        "",
        "## Summary",
        "",
        header_row,
        sep_row,
    ]

    for row in table:
        cells = " | ".join(_score_cell(row, c) for c in ALL_CONDITIONS)
        lines.append(f"| {row['scenario']} | {row['model']} | {cells} |")

    if include_responses:
        lines.extend([
            "",
            "## Raw Responses",
            "",
        ])

        for r in results:
            resp = r.get("response", "")
            if resp == "[DRY RUN]":
                continue
            lines.extend([
                f"### {r['scenario']} / {r['condition']} / {r['model']}",
                "",
                "```",
                resp[:2000] if resp else "(empty)",
                "```",
                "",
            ])

    report = "\n".join(lines)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate naming task eval report")
    parser.add_argument("--results", nargs="+", type=Path, required=True, help="Result JSON files")
    parser.add_argument("--output", type=Path, default=Path("results/naming/report.md"), help="Output report path")
    parser.add_argument("--include-responses", action="store_true", help="Include raw responses in report")
    args = parser.parse_args()

    results = load_results(args.results)
    report = generate_report(results, args.output, include_responses=args.include_responses)
    print(f"Report written to {args.output}")
    print(f"Total results: {len(results)}")
    _ = report


if __name__ == "__main__":
    main()
