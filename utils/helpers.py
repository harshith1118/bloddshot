"""
Utility Helper Functions
Common utilities used across GutCheck.
"""

import json
from typing import Dict, Any, List, Optional


def format_status_emoji(status: str) -> str:
    """Convert status string to emoji."""
    status_map = {
        "GREEN": "🟢",
        "YELLOW": "🟡",
        "RED": "🔴",
        "NORMAL": "✅",
        "BORDERLINE": "⚠️",
        "CONCERN": "🔴"
    }
    return status_map.get(status.upper(), "⚪")


def format_biomarker_status(status: str) -> str:
    """Format biomarker status for display."""
    status_display = {
        "NORMAL": ("✅", "Normal", "green"),
        "BORDERLINE": ("⚠️", "Borderline", "yellow"),
        "CONCERN": ("🔴", "Concern", "red")
    }
    return status_display.get(status.upper(), ("⚪", status, "gray"))


def parse_json_safely(text: str) -> Optional[Dict[str, Any]]:
    """
    Parse JSON from text that may contain markdown or extra content.
    """
    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Try to extract JSON from markdown code block
    import re
    
    # Look for ```json ... ``` blocks
    json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
    match = re.search(json_pattern, text, re.DOTALL)
    
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    
    # Look for any JSON object
    try:
        start = text.find('{')
        end = text.rfind('}') + 1
        if start != -1 and end > start:
            return json.loads(text[start:end])
    except json.JSONDecodeError:
        pass
    
    return None


def calculate_cost_estimate(input_tokens: int, output_tokens: int) -> float:
    """
    Estimate API cost based on token usage.
    
    Mistral Large pricing (check current rates):
    - Input: $2 per 1M tokens
    - Output: $6 per 1M tokens
    """
    input_cost = (input_tokens / 1_000_000) * 2.0
    output_cost = (output_tokens / 1_000_000) * 6.0
    return input_cost + output_cost


def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncate text with ellipsis if too long."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def format_recommendations(recommendations: List[str]) -> str:
    """Format a list of recommendations for display."""
    if not recommendations:
        return "No specific recommendations available."
    
    formatted = []
    for i, rec in enumerate(recommendations, 1):
        formatted.append(f"{i}. {rec}")
    
    return "\n".join(formatted)


def get_status_color_hex(status: str) -> str:
    """Get hex color for status."""
    color_map = {
        "GREEN": "#22c55e",
        "YELLOW": "#eab308",
        "RED": "#ef4444",
        "NORMAL": "#22c55e",
        "BORDERLINE": "#eab308",
        "CONCERN": "#ef4444"
    }
    return color_map.get(status.upper(), "#9ca3af")


def create_analysis_summary(analysis_result: Dict[str, Any]) -> str:
    """Create a quick summary string from analysis results."""
    status = analysis_result.get("overall_status", "Unknown")
    summary = analysis_result.get("summary", "No summary available.")
    biomarkers = analysis_result.get("biomarkers", [])
    
    flagged_count = sum(
        1 for b in biomarkers 
        if b.get("status", "").upper() in ["BORDERLINE", "CONCERN"]
    )
    
    emoji = format_status_emoji(status)
    
    return f"{emoji} {status} - {flagged_count} biomarker(s) need attention\n\n{summary}"
