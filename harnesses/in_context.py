"""In-context harness: inject m4x data into system/user prompt.

All 4 conditions share identical encouragement text. The only variable
is what reference data (if any) accompanies the prompt.
"""

from __future__ import annotations

SHARED_ENCOURAGEMENT = """You are a software architect naming components for a new system. Good component names use a consistent metaphorical frame — all names come from the same source domain (e.g., all from cooking, all from military command, all from theater). This makes the system easier to understand and communicate about.

{system_desc}

Name exactly 10 components. For each, provide:
1. The name (drawn from your chosen metaphorical frame)
2. Which component role it fulfills
3. Why this name fits that role
4. What the name might mislead someone about

Output as a numbered list: Name | Role | Why This Name | Potential Mislead"""

DATA_PREAMBLE = """Here is reference material on metaphorical source domains:

{data_block}

---

"""

CONDITIONS = ["baseline", "frames_only", "m4x_pairs", "m4x_full"]


def build_messages(system_desc: str, condition: str, data_block: str = "") -> list[dict]:
    """Build chat messages for a naming eval condition.

    All conditions get identical SHARED_ENCOURAGEMENT. Non-baseline conditions
    prepend a neutral data block.

    Args:
        system_desc: Description of the system to name components for.
        condition: One of 'baseline', 'frames_only', 'm4x_pairs', 'm4x_full'.
        data_block: Reference data to inject (ignored for baseline).
    """
    if condition not in CONDITIONS:
        raise ValueError(f"Unknown condition: {condition}. Must be one of {CONDITIONS}")

    task = SHARED_ENCOURAGEMENT.format(system_desc=system_desc)

    if condition == "baseline":
        return [{"role": "user", "content": task}]
    else:
        preamble = DATA_PREAMBLE.format(data_block=data_block)
        return [{"role": "user", "content": preamble + task}]
