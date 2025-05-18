"""Azure Speech-to-Text transcription utilities."""

import logging
import threading
import time
from typing import Optional

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:  # pragma: no cover - library may not be installed in all environments
    speechsdk = None  # type: ignore

from .storage import incident_transcripts


class AzureTranscriber:
    """Helper class to interact with Azure Speech-to-Text service."""

    def __init__(self, subscription_key: str, region: str, language: str = "en-US",
                 logger: Optional[logging.Logger] = None) -> None:
        if speechsdk is None:
            raise RuntimeError("azure.cognitiveservices.speech is not installed")

        self.speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
        self.speech_config.speech_recognition_language = language
        self.logger = logger or logging.getLogger(__name__)

    def transcribe_file(self, file_path: str, incident_id: str, max_retries: int = 3) -> None:
        """Transcribe an audio file and store results in incident_transcripts."""
        attempt = 0
        while attempt < max_retries:
            try:
                audio_config = speechsdk.audio.AudioConfig(filename=file_path)
                recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config,
                                                        audio_config=audio_config)

                def recognizing(evt: speechsdk.SpeechRecognitionEventArgs) -> None:
                    text = evt.result.text
                    if text:
                        incident_transcripts[incident_id]["partial"].append(text)
                        self.logger.debug("Incident %s partial: %s", incident_id, text)

                def recognized(evt: speechsdk.SpeechRecognitionEventArgs) -> None:
                    if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                        text = evt.result.text
                        if text:
                            incident_transcripts[incident_id]["final"].append(text)
                            self.logger.info("Incident %s final: %s", incident_id, text)
                    elif evt.result.reason == speechsdk.ResultReason.NoMatch:
                        self.logger.warning("No speech recognized for incident %s", incident_id)

                done = threading.Event()

                def stop(evt: speechsdk.SessionEventArgs) -> None:
                    self.logger.debug("Session stopped for incident %s", incident_id)
                    done.set()

                recognizer.recognizing.connect(recognizing)
                recognizer.recognized.connect(recognized)
                recognizer.session_stopped.connect(stop)
                recognizer.canceled.connect(stop)

                recognizer.start_continuous_recognition()
                done.wait()
                recognizer.stop_continuous_recognition()
                return
            except Exception as exc:  # pragma: no cover - runtime errors handled at execution
                attempt += 1
                wait_time = 2 ** attempt
                self.logger.error("Error transcribing %s on attempt %s: %s", file_path, attempt, exc)
                if attempt >= max_retries:
                    raise
                time.sleep(wait_time)

