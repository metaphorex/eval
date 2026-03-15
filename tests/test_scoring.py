"""Tests for scoring functions. Unit tests use mock LLM output; no API key needed."""

from scoring.frame_consistency import parse_consistency_result
from scoring.structural_fidelity import parse_fidelity_result


def test_parse_consistency_high():
    """All names from same domain -> ratio near 1.0."""
    llm_output = """Head Chef | cooking
Sous Chef | cooking
Prep Station | cooking
Pantry | cooking
Recipe Book | cooking
DOMINANT_DOMAIN: cooking
CONSISTENCY_RATIO: 1.0"""
    result = parse_consistency_result(llm_output)
    assert result["consistency_ratio"] == 1.0
    assert result["dominant_domain"] == "cooking"
    assert len(result["domains"]) == 5


def test_parse_consistency_mixed():
    """Mixed domains -> lower ratio."""
    llm_output = """Head Chef | cooking
Goalkeeper | sports
Neuron | biology
Pantry | cooking
Quarterback | sports
DOMINANT_DOMAIN: cooking
CONSISTENCY_RATIO: 0.4"""
    result = parse_consistency_result(llm_output)
    assert result["consistency_ratio"] == 0.4
    assert len(result["domains"]) == 5


def test_parse_consistency_fraction_format():
    """Handle fraction format like 4/5."""
    llm_output = """A | cooking
B | cooking
C | cooking
D | cooking
E | sports
DOMINANT_DOMAIN: cooking
CONSISTENCY_RATIO: 4/5"""
    result = parse_consistency_result(llm_output)
    assert result["consistency_ratio"] == 0.8


def test_parse_consistency_empty():
    """Empty or unparseable output -> 0.0."""
    result = parse_consistency_result("")
    assert result["consistency_ratio"] == 0.0
    assert result["domains"] == []


def test_parse_fidelity_scores():
    """Parse component-level and average scores."""
    llm_output = """Head Chef | 0.9 | 0.7
Sous Chef | 0.8 | 0.6
Prep Station | 0.7 | 0.8
AVG_FIDELITY: 0.8
AVG_MISLEAD: 0.7"""
    result = parse_fidelity_result(llm_output)
    assert result["fidelity"] == 0.8
    assert result["mislead_quality"] == 0.7
    assert len(result["components"]) == 3


def test_parse_fidelity_empty():
    """Empty output -> zero scores."""
    result = parse_fidelity_result("")
    assert result["fidelity"] == 0.0
    assert result["mislead_quality"] == 0.0
    assert result["components"] == []


def test_parse_fidelity_partial():
    """Handle partial output gracefully."""
    llm_output = """Head Chef | 0.9 | 0.7
AVG_FIDELITY: 0.9"""
    result = parse_fidelity_result(llm_output)
    assert result["fidelity"] == 0.9
    assert result["mislead_quality"] == 0.0  # missing
    assert len(result["components"]) == 1
