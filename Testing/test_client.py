import pytest
from Source_Code.Backend.Backend_connections import app
from unittest.mock import patch, MagicMock


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_supabase():
    with patch("Source_Code.Backend.Backend_connections.get_supabase_client") as mock:
        fake_client = MagicMock()
        mock.return_value = fake_client
        yield fake_client


def test_get_all_recipes(client):
    mock_data = [
        {"recipe_id": 1, "name": "Spaghetti"},
        {"recipe_id": 2, "name": "Tacos"}
    ]

    with patch("Source_Code.Backend.Backend_connections.get_all_recipes", return_value=mock_data):
        response = client.get("/api/recipes")
        assert response.status_code == 200
        assert response.get_json() == mock_data
