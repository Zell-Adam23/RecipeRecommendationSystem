import sys
import os
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), "../Source-Code/Backend"))

from Backend_connections import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_all_recipes(client):
    response = client.get("/api/recipes")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)