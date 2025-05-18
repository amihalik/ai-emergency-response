"""Demonstration script for AzureTranscriber."""

import logging
import os
from src.transcription import AzureTranscriber
from src.storage import incident_transcripts

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    subscription_key = os.environ.get("AZURE_SPEECH_KEY")
    region = os.environ.get("AZURE_SPEECH_REGION")
    audio_file = "path_to_audio.wav"  # Replace with an actual audio file
    incident_id = "demo_incident"

    if not subscription_key or not region:
        raise SystemExit("Please set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION env variables")

    transcriber = AzureTranscriber(subscription_key, region)
    transcriber.transcribe_file(audio_file, incident_id)

    print(incident_transcripts[incident_id])
