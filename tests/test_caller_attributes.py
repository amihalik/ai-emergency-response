from src.caller_attributes import CallerAttributes


def test_caller_attributes_defaults():
    attrs = CallerAttributes()
    assert attrs.gender is None
    assert attrs.age_group is None
    assert attrs.emotional_state is None

