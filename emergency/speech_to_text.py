"""Placeholder speech-to-text service."""

from typing import Any


def transcribe_audio(audio_bytes: bytes) -> str:
    """Simulate transcription of audio data."""
    # In a real implementation this would call Azure Speech service
    if not audio_bytes:
        raise ValueError("No audio data provided")
    return "transcribed audio"
