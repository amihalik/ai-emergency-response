from emergency.flow import process_audio


def test_full_flow():
    result = process_audio(b"audio")
    assert result == {
        "transcript": "transcribed audio",
        "classification": {"incident_type": "fire"},
        "resources": {"resource": "fire truck"},
    }
