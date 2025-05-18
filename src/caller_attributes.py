from dataclasses import dataclass
from typing import Optional

@dataclass
class CallerAttributes:
    """Attributes inferred from a caller's voice."""

    gender: Optional[str] = None
    age_group: Optional[str] = None
    emotional_state: Optional[str] = None

