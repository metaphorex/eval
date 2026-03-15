"""Score structural fidelity: do metaphorical names reflect actual component roles?

Uses LLM-as-judge to evaluate each name-role mapping for accuracy,
and assess the quality of "potential mislead" analysis.
"""

from __future__ import annotations

FIDELITY_PROMPT = """You are evaluating the quality of metaphorical component names for a software system.

For each named component below, score two things on a scale of 0.0 to 1.0:
1. FIDELITY: Does the metaphorical name accurately reflect the component's actual role? (1.0 = perfect fit, 0.0 = completely misleading)
2. MISLEAD_QUALITY: Does the "potential mislead" note identify a genuine, non-obvious risk of the name? (1.0 = insightful, 0.0 = trivial or wrong)

System description: {system_desc}

Component names and analysis:
{response}

Output one line per component: COMPONENT_NAME | FIDELITY_SCORE | MISLEAD_SCORE
Then on a new line: AVG_FIDELITY: <average fidelity score>
Then on a new line: AVG_MISLEAD: <average mislead quality score>"""


def parse_fidelity_result(llm_output: str) -> dict:
    """Parse LLM output to extract fidelity and mislead scores.

    Returns dict with keys: components (list of dicts), fidelity (float),
    mislead_quality (float).
    """
    components: list[dict] = []
    fidelity = 0.0
    mislead_quality = 0.0

    for line in llm_output.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        if "AVG_FIDELITY:" in line:
            try:
                fidelity = float(line.split(":", 1)[-1].strip())
            except ValueError:
                fidelity = 0.0
        elif "AVG_MISLEAD:" in line:
            try:
                mislead_quality = float(line.split(":", 1)[-1].strip())
            except ValueError:
                mislead_quality = 0.0
        elif "|" in line:
            parts = line.split("|")
            if len(parts) >= 3:
                name = parts[0].strip().lstrip("0123456789.- ")
                try:
                    f_score = float(parts[1].strip())
                    m_score = float(parts[2].strip())
                    components.append({
                        "name": name,
                        "fidelity": f_score,
                        "mislead_quality": m_score,
                    })
                except ValueError:
                    continue

    return {
        "components": components,
        "fidelity": fidelity,
        "mislead_quality": mislead_quality,
    }


def score_structural_fidelity(
    response: str, system_desc: str, client: object = None,
) -> dict:
    """Use LLM-as-judge to score structural fidelity and mislead quality.

    Args:
        response: The naming task response text to score.
        system_desc: Description of the system being named.
        client: An OpenAI-compatible client (e.g. OpenRouter). If None, creates one.

    Returns:
        Dict with 'fidelity' and 'mislead_quality' scores (0.0-1.0).
    """
    if client is None:
        from scoring.client import make_scoring_client

        client = make_scoring_client()

    from scoring.client import SCORING_MODEL

    result = client.chat.completions.create(
        model=SCORING_MODEL,
        max_tokens=1500,
        messages=[{
            "role": "user",
            "content": FIDELITY_PROMPT.format(
                system_desc=system_desc, response=response,
            ),
        }],
    )
    text = result.choices[0].message.content
    parsed = parse_fidelity_result(text)
    return {
        "fidelity": parsed["fidelity"],
        "mislead_quality": parsed["mislead_quality"],
    }
