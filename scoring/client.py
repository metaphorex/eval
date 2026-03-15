"""Shared OpenRouter client for scoring. Single API key, single provider."""

from __future__ import annotations

import os

from openai import OpenAI

SCORING_MODEL = "google/gemini-2.5-flash-lite"


def make_scoring_client() -> OpenAI:
    """Create an OpenAI client configured for OpenRouter scoring."""
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get("OPENROUTER_API_KEY", ""),
        default_headers={
            "HTTP-Referer": "https://github.com/metaphorex/eval",
            "X-Title": "Metaphorex Eval Scoring",
        },
    )
