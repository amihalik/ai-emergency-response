# incident_classifier.py

"""Module for classifying emergency incidents using Azure OpenAI GPT."""

from dataclasses import dataclass, field
from typing import List, Optional
import json
import os

import openai


@dataclass
class IncidentRecord:
    """Data structure for storing incident information."""

    transcription: str
    background_noises: List[str] = field(default_factory=list)
    classification: Optional[str] = None
    severity: Optional[str] = None
    nature: Optional[str] = None
    num_people_involved: Optional[int] = None


def _build_prompt(transcription: str, noises: List[str]) -> str:
    """Construct the prompt to send to GPT."""
    noise_description = ", ".join(noises) if noises else "none"
    return (
        "You are an emergency incident classification assistant.\n"
        "Given the caller transcription and important background noises, "
        "identify the type of incident, severity, nature of the incident, "
        "and number of people involved.\n"
        "Provide your answer strictly as valid JSON in the following format:\n"
        "{\n"
        "  \"category\": <incident category>,\n"
        "  \"severity\": <incident severity>,\n"
        "  \"nature\": <short description>,\n"
        "  \"num_people_involved\": <number or null>\n"
        "}\n"
        f"Transcription: {transcription}\n"
        f"Background noises: {noise_description}"
    )


def classify_incident(transcription: str, noises: Optional[List[str]] = None) -> IncidentRecord:
    """Use Azure OpenAI GPT to classify an incident and extract key details."""
    if noises is None:
        noises = []

    prompt = _build_prompt(transcription, noises)

    # Configure OpenAI/Azure OpenAI parameters via environment variables
    api_key = os.getenv("AZURE_OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-35-turbo")

    if not api_key:
        raise RuntimeError("OpenAI API key not configured")

    openai.api_type = "azure" if api_base else "open_ai"
    if api_base:
        openai.api_key = api_key
        openai.api_base = api_base
        openai.api_version = api_version
    else:
        openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model=deployment,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError(f"Failed to parse GPT response: {content}")

    record = IncidentRecord(
        transcription=transcription,
        background_noises=noises,
        classification=data.get("category"),
        severity=data.get("severity"),
        nature=data.get("nature"),
        num_people_involved=data.get("num_people_involved"),
    )
    return record
