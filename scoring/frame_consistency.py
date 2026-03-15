"""Score frame consistency: do all names come from the same source domain?

Uses LLM-as-judge to extract source domains from component names,
then computes the ratio of names in the dominant domain.
"""

from __future__ import annotations

EXTRACTION_PROMPT = """Analyze these component names from a software system and identify which metaphorical source domain each name comes from.

{response}

For each name, output one line: NAME | SOURCE_DOMAIN
Then on a new line output: DOMINANT_DOMAIN: <the most common domain>
Then on a new line output: CONSISTENCY_RATIO: <count of names in dominant domain / total names as a decimal>"""


def parse_consistency_result(llm_output: str) -> dict:
    """Parse LLM output to extract domains and consistency ratio.

    Returns dict with keys: domains (list of (name, domain) tuples),
    dominant_domain (str), consistency_ratio (float).
    """
    domains = []
    dominant_domain = ""
    consistency_ratio = 0.0

    for line in llm_output.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        if "DOMINANT_DOMAIN:" in line:
            dominant_domain = line.split(":", 1)[-1].strip()
        elif "CONSISTENCY_RATIO:" in line:
            try:
                val = line.split(":", 1)[-1].strip()
                # Handle fraction format like "4/5"
                if "/" in val:
                    num, den = val.split("/")
                    consistency_ratio = float(num.strip()) / float(den.strip())
                else:
                    consistency_ratio = float(val)
            except (ValueError, ZeroDivisionError):
                consistency_ratio = 0.0
        elif "|" in line:
            parts = line.split("|")
            if len(parts) >= 2:
                name = parts[0].strip().lstrip("0123456789.- ")
                domain = parts[1].strip()
                if name and domain:
                    domains.append((name, domain))

    return {
        "domains": domains,
        "dominant_domain": dominant_domain,
        "consistency_ratio": consistency_ratio,
    }


def score_frame_consistency(response: str, client=None) -> float:
    """Use LLM to extract source domains and compute consistency ratio.

    Args:
        response: The naming task response text to score.
        client: An Anthropic client instance. If None, creates one.

    Returns:
        Float between 0.0 and 1.0 representing frame consistency.
    """
    if client is None:
        from anthropic import Anthropic

        client = Anthropic()

    result = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": EXTRACTION_PROMPT.format(response=response)}
        ],
    )
    text = result.content[0].text
    parsed = parse_consistency_result(text)
    return parsed["consistency_ratio"]
