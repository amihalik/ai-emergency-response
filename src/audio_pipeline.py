"""Audio processing pipeline functions."""
from typing import List

from .incident import Incident, BackgroundNoise
from .background_noise_classifier import classify_background_noises


def transcribe_audio(audio_path: str) -> str:
    """Convert speech in the audio file to text.

    This is a minimal placeholder implementation. Integrating Azure Speech-to-Tex
    t should replace this.
    """
    # TODO: integrate Azure Speech-to-Text service
    return "example transcript"


def process_audio_file(audio_path: str) -> Incident:
    """Process an audio file and return populated Incident data."""
    incident = Incident()

    # Speech-to-text and background noise classification happen in the same step
    incident.transcript = transcribe_audio(audio_path)
    detections = classify_background_noises(audio_path)

    for d in detections:
        incident.background_noises.append(BackgroundNoise(**d))

    return incident
