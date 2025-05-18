import os
from dataclasses import dataclass
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    speech_endpoint: str | None = os.getenv("AZURE_SPEECH_ENDPOINT")
    speech_key: str | None = os.getenv("AZURE_SPEECH_KEY")
    audio_endpoint: str | None = os.getenv("AZURE_AUDIO_ENDPOINT")
    audio_key: str | None = os.getenv("AZURE_AUDIO_KEY")
    openai_endpoint: str | None = os.getenv("AZURE_OPENAI_ENDPOINT")
    openai_key: str | None = os.getenv("AZURE_OPENAI_KEY")

@lru_cache()
def get_settings() -> Settings:
    return Settings()
