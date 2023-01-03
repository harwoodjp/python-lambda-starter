import json
from unittest.mock import Mock

from app import write

from lib.dynamo_client import DynamoClient


def test_write_returns_item():
    dynamo_client = Mock(DynamoClient)
    dynamo_client.put_item.return_value = None
    response = write(body={"message": "Hello!"}, dynamo_client=dynamo_client)
    assert response.get("id") and response.get("message")
    assert response.get("message") == "Hello!"