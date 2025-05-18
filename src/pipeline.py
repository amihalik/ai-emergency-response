"""Simple processing pipeline for emergency call audio."""
from pathlib import Path
from typing import Optional

import azure.cognitiveservices.speech as speechsdk

from .attribute_analyzer import CallerAttributeAnalyzer
from .caller_attributes import CallerAttributes


def transcribe_audio(audio_path: str, speech_key: str, speech_region: str) -> str:
    """Transcribe the given audio file using Azure Speech-to-Text."""
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    audio_config = speechsdk.audio.AudioConfig(filename=audio_path)
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    return ""


def process_audio_call(audio_path: str, speech_key: str, speech_region: str) -> tuple[str, CallerAttributes]:
    """Transcribe an emergency call and infer caller attributes."""
    transcription = transcribe_audio(audio_path, speech_key, speech_region)
    analyzer = CallerAttributeAnalyzer(speech_key, speech_region)
    attributes = analyzer.analyze(audio_path)
    return transcription, attributes

