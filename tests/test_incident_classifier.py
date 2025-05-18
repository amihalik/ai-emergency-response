import json
from incident_classifier import classify_incident

class FakeResponse:
    def __init__(self, content):
        self.choices = [type('obj', (object,), {'message': type('obj', (object,), {'content': content})})]

def fake_chat_completion_create(model, messages, temperature):
    assert model
    assert messages
    return FakeResponse('{"category": "fire", "severity": "high", "nature": "house fire", "num_people_involved": 3}')

def test_classify_incident(monkeypatch):
    monkeypatch.setattr('openai.ChatCompletion.create', fake_chat_completion_create)
    record = classify_incident('There is smoke everywhere', ['fire alarm'])
    assert record.classification == 'fire'
    assert record.severity == 'high'
    assert record.nature == 'house fire'
    assert record.num_people_involved == 3
