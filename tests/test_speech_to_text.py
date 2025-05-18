from emergency.speech_to_text import transcribe_audio


def test_transcribe_audio():
    result = transcribe_audio(b"audio")
    assert result == "transcribed audio"
