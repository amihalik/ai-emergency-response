from emergency.resource_assignment import assign_resources


def test_assign_resources():
    result = assign_resources({"incident_type": "fire"})
    assert result == {"resource": "fire truck"}
