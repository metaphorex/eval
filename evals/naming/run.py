"""Run the naming task eval across conditions and models."""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

from openai import OpenAI

from data.snapshot import load_snapshot
from data.transform import to_context_block, to_frames_list, to_pairs_block
from evals.naming.task import SCENARIOS
from harnesses.in_context import CONDITIONS, build_messages

RESULTS_DIR = Path("results/naming")

OPENROUTER_MODELS = {
    "deepseek-v3": "deepseek/deepseek-chat-v3-0324",
    "gemini-flash-lite": "google/gemini-2.5-flash-lite",
    "qwen3.5-9b": "qwen/qwen3.5-9b",
    "gpt5-nano": "openai/gpt-5-nano",
    "gemma-3-27b": "google/gemma-3-27b-it",
}


def _make_openrouter_client() -> OpenAI:
    """Create an OpenAI client configured for OpenRouter."""
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get("OPENROUTER_API_KEY", ""),
        default_headers={
            "HTTP-Referer": "https://github.com/metaphorex/eval",
            "X-Title": "Metaphorex Eval",
        },
    )


def _build_data_blocks(mappings: list[dict]) -> dict[str, str]:
    """Build the data block string for each condition."""
    return {
        "baseline": "",
        "frames_only": to_frames_list(mappings),
        "m4x_pairs": to_pairs_block(mappings),
        "m4x_full": to_context_block(mappings),
    }


def run_single(
    scenario,
    condition: str,
    model_key: str,
    data_blocks: dict[str, str],
    dry_run: bool = False,
) -> dict:
    """Run a single eval: one scenario x one condition x one model."""
    data_block = data_blocks.get(condition, "")
    msgs = build_messages(scenario.system_desc, condition, data_block)

    if dry_run:
        return {
            "scenario": scenario.name,
            "condition": condition,
            "model": model_key,
            "messages": [
                {"role": m["role"], "content": m["content"][:200] + "..."}
                for m in msgs
            ],
            "response": "[DRY RUN]",
        }

    model_id = OPENROUTER_MODELS[model_key]
    client = _make_openrouter_client()
    resp = client.chat.completions.create(
        model=model_id,
        max_tokens=2000,
        messages=msgs,
    )
    text = resp.choices[0].message.content
    return {
        "scenario": scenario.name,
        "condition": condition,
        "model": model_key,
        "model_id": model_id,
        "response": text,
        "usage": {
            "prompt_tokens": resp.usage.prompt_tokens if resp.usage else None,
            "completion_tokens": (
                resp.usage.completion_tokens if resp.usage else None
            ),
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Run the naming task eval")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print messages without calling API",
    )
    snapshot_group = parser.add_mutually_exclusive_group(required=True)
    snapshot_group.add_argument(
        "--snapshot",
        type=Path,
        help="Path to m4x snapshot JSON",
    )
    snapshot_group.add_argument(
        "--snapshot-version",
        type=str,
        help="CalVer version to fetch from GitHub releases (e.g. 2026.03.14)",
    )
    parser.add_argument(
        "--models",
        nargs="+",
        default=list(OPENROUTER_MODELS.keys()),
        help="Models to eval",
    )
    parser.add_argument(
        "--conditions",
        nargs="+",
        default=CONDITIONS,
        help="Conditions to test",
    )
    parser.add_argument(
        "--scenarios",
        nargs="+",
        default=None,
        help="Scenario names (default: all)",
    )
    args = parser.parse_args()

    if args.snapshot_version:
        from data.snapshot import fetch_snapshot

        snapshot_path = fetch_snapshot(version=args.snapshot_version)
    else:
        snapshot_path = args.snapshot

    mappings = load_snapshot(snapshot_path)
    data_blocks = _build_data_blocks(mappings)

    scenarios = SCENARIOS
    if args.scenarios:
        scenarios = [s for s in SCENARIOS if s.name in args.scenarios]

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for scenario in scenarios:
        for condition in args.conditions:
            for model in args.models:
                print(f"Running: {scenario.name} / {condition} / {model}")
                result = run_single(
                    scenario,
                    condition,
                    model,
                    data_blocks,
                    args.dry_run,
                )
                results.append(result)
                if not args.dry_run:
                    time.sleep(1)

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    out = RESULTS_DIR / f"run-{timestamp}.json"
    out.write_text(json.dumps(results, indent=2))
    print(f"\nResults saved to {out}")
    print(f"Total runs: {len(results)}")


if __name__ == "__main__":
    main()
