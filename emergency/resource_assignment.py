"""Placeholder resource assignment service."""

from typing import Dict


def assign_resources(classification: Dict[str, str]) -> Dict[str, str]:
    """Simulate assigning emergency resources based on classification."""
    if not classification.get("incident_type"):
        raise ValueError("No incident type provided")
    return {"resource": "fire truck"}
