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


def test_get_recipe_by_id_success(client):
    recipe = {"recipe_id": 1, "name": "Spaghetti"}

    with patch(
        "Source_Code.Backend.Backend_connections.get_recipe_by_id",
        return_value=recipe,
    ):
        response = client.get("/api/recipes/1")

    assert response.status_code == 200
    assert response.get_json() == recipe


def test_get_recipe_by_id_not_found(client):
    with patch(
        "Source_Code.Backend.Backend_connections.get_recipe_by_id",
        return_value=None,
    ):
        response = client.get("/api/recipes/999")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Recipe Not Found"


def test_search_recipe(client):
    results = [{"recipe_id": 1, "name": "Spaghetti"}]

    with patch(
        "Source_Code.Backend.Backend_connections.search_recipe",
        return_value=results,
    ):
        response = client.post(
            "/api/recipes/search",
            json={"query": "Spa"},
        )

    assert response.status_code == 200
    assert response.get_json() == results


def test_get_user_by_id(client):
    user = {"user_id": 1, "display_name": "Adam"}

    with patch(
        "Source_Code.Backend.Backend_connections.get_user_by_id",
        return_value=user,
    ):
        response = client.get("/api/users/1")

    assert response.status_code == 200
    assert response.get_json() == user


def test_get_saved_recipes(client):
    saved = [{"recipe_id": 2, "name": "Tacos"}]

    with patch(
        "Source_Code.Backend.Backend_connections.get_saved_recipes",
        return_value=saved,
    ):
        response = client.get("/api/saved-recipes/1")

    assert response.status_code == 200
    assert response.get_json() == saved


def test_insert_recipe(client):
    result = {"recipe_id": 3, "name": "Pizza"}

    with patch(
        "Source_Code.Backend.Backend_connections.insert_recipe",
        return_value=result,
    ):
        response = client.post(
            "/api/recipes",
            json={"name": "Pizza"},
        )

    assert response.status_code == 201
    assert response.get_json() == result


def test_edit_recipe(client):
    updated = {"recipe_id": 1, "name": "Updated"}

    with patch(
        "Source_Code.Backend.Backend_connections.edit_recipe",
        return_value=updated,
    ):
        response = client.post(
            "/api/recipes/edit",
            json={"recipe_id": 1, "name": "Updated"},
        )

    assert response.status_code == 200
    assert response.get_json() == updated


def test_register_user_success(client):
    user = {"user_id": 1, "display_name": "Adam"}

    with patch(
        "Source_Code.Backend.Backend_connections.register_user",
        return_value=user,
    ):
        response = client.post(
            "/api/users",
            json={"email": "a@test.com", "password_hash": "hashed"},
        )

    assert response.status_code == 201
    assert response.get_json() == user


def test_register_user_error(client):
    error = ({"error": "email exists"}, 400)

    with patch(
        "Source_Code.Backend.Backend_connections.register_user",
        return_value=error,
    ):
        response = client.post(
            "/api/users",
            json={"email": "a@test.com", "password_hash": "hashed"},
        )

    assert response.status_code == 400
    assert response.get_json()["error"] == "email exists"


def test_authenticate_success(client, mock_supabase):
    # Mock authentication result
    with patch(
        "Source_Code.Backend.Backend_connections.authenticate",
        return_value=1,
    ):
        # Mock Supabase chained calls
        user_data = MagicMock()
        user_data.data = {"display_name": "Adam"}

        user_auth = MagicMock()
        user_auth.data = {"email": "a@test.com"}

        mock_supabase.table.return_value.select.return_value.eq.return_value.single.return_value.execute.side_effect = [
            user_data,
            user_auth,
        ]

        response = client.post(
            "/api/users/authenticate",
            json={"email": "a@test.com", "password_hash": "hashed"},
        )

    assert response.status_code == 200
    body = response.get_json()
    assert body["display_name"] == "Adam"
    assert body["email"] == "a@test.com"


def test_authenticate_failure(client):
    with patch(
        "Source_Code.Backend.Backend_connections.authenticate",
        return_value=None,
    ):
        response = client.post(
            "/api/users/authenticate",
            json={"email": "a@test.com", "password_hash": "wrong"},
        )

    assert response.status_code == 401
    assert response.get_json()["error"] == "invalid credentials"


def test_save_recipe_success(client):
    result = {"saved": True}

    with patch(
        "Source_Code.Backend.Backend_connections.save_recipe",
        return_value=result,
    ):
        response = client.post(
            "/api/saved-recipes",
            json={"user_id": 1, "recipe_id": 2},
        )

    assert response.status_code == 201
    assert response.get_json() == result


def test_save_recipe_error(client):
    error = ({"error": "already saved"}, 400)

    with patch(
        "Source_Code.Backend.Backend_connections.save_recipe",
        return_value=error,
    ):
        response = client.post(
            "/api/saved-recipes",
            json={"user_id": 1, "recipe_id": 2},
        )

    assert response.status_code == 400
    assert response.get_json()["error"] == "already saved"


def test_unsave_recipe_success(client):
    result = {"unsaved": True}

    with patch(
        "Source_Code.Backend.Backend_connections.unsave_recipe",
        return_value=result,
    ):
        response = client.delete(
            "/api/saved-recipes",
            json={"user_id": 1, "recipe_id": 2},
        )

    assert response.status_code == 200
    assert response.get_json() == result