from emergency.gpt_classifier import classify_incident


def test_classify_incident():
    result = classify_incident("some transcript")
    assert result == {"incident_type": "fire"}
