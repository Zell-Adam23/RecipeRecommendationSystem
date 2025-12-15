import pytest
from Source_Code.Backend.backend_connections import app
from unittest.mock import patch


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_all_recipes(client):
    mock_data = [
        {"recipe_id": 1, "name": "Spaghetti"},
        {"recipe_id": 2, "name": "Tacos"}
    ]

    with patch("Source_Code.Backend.backend_connections.get_all_recipes", return_value=mock_data):
        response = client.get("/api/recipes")
        assert response.status_code == 200
        assert response.get_json() == mock_data
