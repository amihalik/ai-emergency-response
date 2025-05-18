from dataclasses import dataclass, field
from typing import List

@dataclass
class BackgroundNoise:
    """Represents a single detected background sound."""
    label: str
    timestamp: float
    confidence: float

@dataclass
class Incident:
    """Data collected from a single emergency call."""
    transcript: str = ""
    background_noises: List[BackgroundNoise] = field(default_factory=list)
