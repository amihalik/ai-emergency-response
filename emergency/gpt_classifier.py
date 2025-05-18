"""Placeholder GPT-based incident classification."""

from typing import Dict


def classify_incident(transcript: str) -> Dict[str, str]:
    """Simulate incident classification using GPT."""
    # Real implementation would call Azure OpenAI
    if not transcript:
        raise ValueError("Transcript is empty")
    return {"incident_type": "fire"}
