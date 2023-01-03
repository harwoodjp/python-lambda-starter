import json

from functions.string_reverser.app import handler, reverse


def test_handler():
    event = {"resource": "/reverse", "path": "/reverse/backwards", "httpMethod": "GET"}
    response = handler(event, None)
    body = json.loads(response.get("body"))
    result = body.get("result")
    assert result == "sdrawkcab"


def test_reverse_string_response():
    response = reverse("backwards")
    assert response.get("result") == "sdrawkcab"