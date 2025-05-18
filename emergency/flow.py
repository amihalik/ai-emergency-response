"""Module orchestrating the incident processing flow."""

from typing import Dict

from .speech_to_text import transcribe_audio
from .gpt_classifier import classify_incident
from .resource_assignment import assign_resources


def process_audio(audio_bytes: bytes) -> Dict[str, str]:
    """Run the full incident processing flow."""
    transcript = transcribe_audio(audio_bytes)
    classification = classify_incident(transcript)
    resources = assign_resources(classification)
    return {"transcript": transcript, "classification": classification, "resources": resources}
