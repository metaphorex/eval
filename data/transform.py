"""Transform snapshot data into eval-friendly formats."""

from __future__ import annotations


def to_pairs(mappings: list[dict]) -> list[dict]:
    """Extract (source, target, expressions, where_it_breaks) pairs."""
    return [
        {
            "slug": m["slug"],
            "name": m["name"],
            "kind": m["kind"],
            "source_frame": m["source_frame"],
            "target_frame": m["target_frame"],
            "expressions": m.get("sections", {}).get("Expressions", ""),
            "where_it_breaks": m.get("sections", {}).get("Where It Breaks", ""),
            "what_it_brings": m.get("sections", {}).get("What It Brings", ""),
        }
        for m in mappings
    ]


def to_context_block(mappings: list[dict]) -> str:
    """Format all mappings as a single context block for in-context injection."""
    lines = []
    for m in mappings:
        sections = m.get("sections", {})
        lines.append(f"## {m['name']} ({m['kind']})")
        lines.append(f"Source: {m['source_frame']} → Target: {m['target_frame']}")
        for section_name in ["What It Brings", "Where It Breaks", "Expressions"]:
            if section_name in sections:
                lines.append(f"### {section_name}")
                lines.append(sections[section_name])
        lines.append("")
    return "\n".join(lines)


def to_frames_list(mappings: list[dict]) -> str:
    """Extract unique source frame names as a bullet list.

    Used for the 'frames_only' condition — gives the model ~20 source domain
    names without any mapping detail.
    """
    frames = sorted({m["source_frame"] for m in mappings})
    return "\n".join(f"- {frame}" for frame in frames)


def to_pairs_block(mappings: list[dict]) -> str:
    """Format mappings as compact name + source→target lines.

    Used for the 'm4x_pairs' condition.
    """
    lines = []
    for m in mappings:
        lines.append(f"- **{m['name']}** ({m['kind']}): {m['source_frame']} → {m['target_frame']}")
    return "\n".join(lines)
