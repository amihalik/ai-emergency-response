"""Background noise classification utilities."""
from typing import List, Dict


def classify_background_noises(audio_path: str) -> List[Dict[str, float]]:
    """Classify background noises in the given audio file.

    This implementation is a placeholder. In a production system, this function
    would call Azure's Audio Classification service or a custom ML model.

    Parameters
    ----------
    audio_path: str
        Path to the audio file to analyze.

    Returns
    -------
    List of detections. Each detection is a dictionary with keys:
    'label', 'timestamp', and 'confidence'.
    """

    # TODO: integrate Azure or custom ML model for real classification
    # Example static output for demonstration purposes
    return [
        {"label": "gunshot", "timestamp": 3.5, "confidence": 0.92},
        {"label": "alarm", "timestamp": 15.2, "confidence": 0.88},
    ]
