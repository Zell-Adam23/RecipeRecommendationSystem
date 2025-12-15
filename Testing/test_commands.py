import pytest
from unittest.mock import MagicMock, patch

from Source_Code.Backend.Commands.authentiate_user import authenticate
from Source_Code.Backend.Commands.create_recipe import insert_recipe
from Source_Code.Backend.Commands.edit_recipe import edit_recipe
from Source_Code.Backend.Commands.register_user import register_user
from Source_Code.Backend.Commands.save_recipe import save_recipe
from Source_Code.Backend.Commands.unsave_recipe import unsave_recipe
from Source_Code.Backend.Commands.add_pantry_item import add_pantry_item
from Source_Code.Backend.Commands.remove_pantry_item import remove_pantry_item


def test_authenticate_user_not_found_returns_none():
    mock_response = MagicMock()
    mock_response.data = None

    mock_client = MagicMock()
    (
        mock_client.table.return_value
        .select.return_value
        .eq.return_value
        .single.return_value
        .execute.return_value
    ) = mock_response

    with patch(
        "Source_Code.Backend.Commands.authentiate_user.get_supabase_client",
        return_value=mock_client,
    ):
        result = authenticate("test@example.com", "password")

    assert result is None


def test_authenticate_success_returns_user_id():
    mock_response = MagicMock()
    mock_response.data = {
        "user_id": 1,
        "email": "test@example.com",
        "password_hash": "hashedpw",
    }

    mock_client = MagicMock()
    (
        mock_client.table.return_value
        .select.return_value
        .eq.return_value
        .single.return_value
        .execute.return_value
    ) = mock_response

    with patch(
        "Source_Code.Backend.Commands.authentiate_user.get_supabase_client",
        return_value=mock_client,
    ), patch(
        "Source_Code.Backend.Commands.authentiate_user.bcrypt.checkpw",
        return_value=True,
    ):
        result = authenticate("test@example.com", "password")

    assert result == 1


def test_authenticate_invalid_password_returns_none():
    mock_response = MagicMock()
    mock_response.data = {
        "user_id": 1,
        "email": "test@example.com",
        "password_hash": "hashedpw",
    }

    mock_client = MagicMock()
    (
        mock_client.table.return_value
        .select.return_value
        .eq.return_value
        .single.return_value
        .execute.return_value
    ) = mock_response

    with patch(
        "Source_Code.Backend.Commands.authentiate_user.get_supabase_client",
        return_value=mock_client,
    ), patch(
        "Source_Code.Backend.Commands.authentiate_user.bcrypt.checkpw",
        return_value=False,
    ):
        result = authenticate("test@example.com", "wrongpassword")

    assert result is None


def test_authenticate_exception_returns_none():
    mock_client = MagicMock()
    mock_client.table.side_effect = Exception("DB error")

    with patch(
        "Source_Code.Backend.Commands.authentiate_user.get_supabase_client",
        return_value=mock_client,
    ):
        result = authenticate("test@example.com", "password")

    assert result is None


def test_insert_recipe_success_returns_created_recipe():
    input_data = {
        "title": "Pancakes",
        "short_description": "Fluffy pancakes",
        "is_public": False,
    }

    mock_response = MagicMock()
    mock_response.data = [
        {
            "recipe_id": 1,
            "title": "Pancakes",
            "short_description": "Fluffy pancakes",
            "is_public": False,
            "created_at": "2025-01-01T00:00:00Z",
        }
    ]

    mock_client = MagicMock()
    mock_client.table.return_value.insert.return_value.execute.return_value = mock_response

    with patch(
        "Source_Code.Backend.Commands.create_recipe.get_supabase_client",
        return_value=mock_client,
    ):
        result = insert_recipe(input_data)

    assert result["recipe_id"] == 1
    assert result["title"] == "Pancakes"


def test_insert_recipe_failure_returns_none():
    input_data = {
        "title": "Waffles",
        "short_description": "Crispy waffles",
    }

    mock_response = MagicMock()
    mock_response.data = None

    mock_client = MagicMock()
    mock_client.table.return_value.insert.return_value.execute.return_value = mock_response

    with patch(
        "Source_Code.Backend.Commands.create_recipe.get_supabase_client",
        return_value=mock_client,
    ):
        result = insert_recipe(input_data)

    assert result is None


def test_edit_recipe_returns_updated_data():
    mock_response = MagicMock()
    mock_response.data = [
        {
            "recipe_id": 1,
            "title": "Updated Pancakes",
            "is_public": True,
        }
    ]

    mock_client = MagicMock()
    (
        mock_client.table.return_value
        .update.return_value
        .eq.return_value
        .execute.return_value
    ) = mock_response

    with patch(
        "Source_Code.Backend.Commands.edit_recipe.get_supabase_client",
        return_value=mock_client,
    ):
        result = edit_recipe(1, {"title": "Updated Pancakes"})

    assert result == mock_response.data


def test_register_user_missing_fields_returns_400():
    result, status = register_user({"email": "a@test.com"})

    assert status == 400
    assert result["error"] == "Missing required fields"


def test_register_user_email_exists_returns_409():
    mock_existing = MagicMock()
    mock_existing.data = [{"email": "a@test.com"}]

    mock_client = MagicMock()
    mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_existing

    with patch(
        "Source_Code.Backend.Commands.register_user.get_supabase_client",
        return_value=mock_client,
    ):
        result, status = register_user({
            "email": "a@test.com",
            "password_hash": "password",
            "display_name": "Adam",
        })

    assert status == 409
    assert result["error"] == "Email already exists"


def test_register_user_account_creation_failure_returns_500():
    mock_existing = MagicMock()
    mock_existing.data = []

    mock_user_response = MagicMock()
    mock_user_response.data = None

    mock_client = MagicMock()
    mock_client.table.side_effect = [
        # USER_AUTH exists check
        MagicMock(select=MagicMock(return_value=MagicMock(eq=MagicMock(return_value=MagicMock(execute=MagicMock(return_value=mock_existing)))))),
        # USER_ACCOUNT insert
        MagicMock(insert=MagicMock(return_value=MagicMock(execute=MagicMock(return_value=mock_user_response)))),
    ]

    with patch(
        "Source_Code.Backend.Commands.register_user.get_supabase_client",
        return_value=mock_client,
    ), patch(
        "Source_Code.Backend.Commands.register_user.bcrypt.gensalt",
        return_value=b"salt",
    ), patch(
        "Source_Code.Backend.Commands.register_user.bcrypt.hashpw",
        return_value=b"hashed",
    ):
        result, status = register_user({
            "email": "a@test.com",
            "password_hash": "password",
            "display_name": "Adam",
        })

    assert status == 500
    assert result["error"] == "Failed to create user account"


def test_register_user_auth_creation_failure_rolls_back():
    mock_existing = MagicMock()
    mock_existing.data = []

    mock_user_response = MagicMock()
    mock_user_response.data = [{"user_id": 1}]

    mock_auth_response = MagicMock()
    mock_auth_response.data = None

    mock_client = MagicMock()
    mock_client.table.side_effect = [
        # USER_AUTH exists check
        MagicMock(select=MagicMock(return_value=MagicMock(eq=MagicMock(return_value=MagicMock(execute=MagicMock(return_value=mock_existing)))))),
        # USER_ACCOUNT insert
        MagicMock(insert=MagicMock(return_value=MagicMock(execute=MagicMock(return_value=mock_user_response)))),

        # USER_AUTH insert
        MagicMock(insert=MagicMock(return_value=MagicMock(execute=MagicMock(return_value=mock_auth_response)))),

        # USER_ACCOUNT delete rollback
        MagicMock(delete=MagicMock(return_value=MagicMock(eq=MagicMock(return_value=MagicMock(execute=MagicMock()))))),
    ]

    with patch(
        "Source_Code.Backend.Commands.register_user.get_supabase_client",
        return_value=mock_client,
    ), patch(
        "Source_Code.Backend.Commands.register_user.bcrypt.gensalt",
        return_value=b"salt",
    ), patch(
        "Source_Code.Backend.Commands.register_user.bcrypt.hashpw",
        return_value=b"hashed",
    ):
        result, status = register_user({
            "email": "a@test.com",
            "password_hash": "password",
            "display_name": "Adam",
        })

    assert status == 500
    assert result["error"] == "Failed to create authentication record"



def test_register_user_success_returns_user_data():
    mock_existing = MagicMock()
    mock_existing.data = []

    mock_user_response = MagicMock()
    mock_user_response.data = [{"user_id": 1}]

    mock_auth_response = MagicMock()
    mock_auth_response.data = [{"user_id": 1}]

    mock_client = MagicMock()
    mock_client.table.side_effect = [
        # USER_AUTH exists check
        MagicMock(select=MagicMock(return_value=MagicMock(eq=MagicMock(return_value=MagicMock(execute=MagicMock(return_value=mock_existing)))))),
        # USER_ACCOUNT insert
        MagicMock(insert=MagicMock(return_value=MagicMock(execute=MagicMock(return_value=mock_user_response)))),
        # USER_AUTH insert
        MagicMock(insert=MagicMock(return_value=MagicMock(execute=MagicMock(return_value=mock_auth_response)))),
    ]

    with patch(
        "Source_Code.Backend.Commands.register_user.get_supabase_client",
        return_value=mock_client,
    ), patch(
        "Source_Code.Backend.Commands.register_user.bcrypt.gensalt",
        return_value=b"salt",
    ), patch(
        "Source_Code.Backend.Commands.register_user.bcrypt.hashpw",
        return_value=b"hashed",
    ):
        result = register_user({
            "email": "a@test.com",
            "password_hash": "password",
            "display_name": "Adam",
        })

    assert result["user_id"] == 1
    assert result["email"] == "a@test.com"
    assert result["display_name"] == "Adam"


def test_save_recipe_missing_user_or_recipe_returns_400():
    result, status = save_recipe(None, 1)
    assert status == 400
    assert result["error"] == "Missing user_id or recipe_id"

    result, status = save_recipe(1, None)
    assert status == 400
    assert result["error"] == "Missing user_id or recipe_id"


def test_save_recipe_recipe_not_found_returns_404():
    mock_recipe_check = MagicMock()
    mock_recipe_check.data = None

    mock_client = MagicMock()
    mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_recipe_check

    with patch(
        "Source_Code.Backend.Commands.save_recipe.get_supabase_client",
        return_value=mock_client,
    ):
        result, status = save_recipe(1, 99)

    assert status == 404
    assert result["error"] == "Recipe not found"


def test_save_recipe_already_saved_returns_409():
    # Recipe exists
    mock_recipe_check = MagicMock()
    mock_recipe_check.data = [{"recipe_id": 1}]

    # Already saved
    mock_existing = MagicMock()
    mock_existing.data = [{"user_id": 1, "recipe_id": 1, "relation_type": "saved"}]

    mock_client = MagicMock()
    mock_client.table.side_effect = [
        # Recipe check
        MagicMock(select=MagicMock(return_value=MagicMock(eq=MagicMock(return_value=MagicMock(execute=MagicMock(return_value=mock_recipe_check)))))),
        # Existing check
        MagicMock(select=MagicMock(return_value=MagicMock(eq=MagicMock(return_value=MagicMock(eq=MagicMock(return_value=MagicMock(eq=MagicMock(return_value=MagicMock(execute=MagicMock(return_value=mock_existing)))))))))),
    ]

    with patch(
        "Source_Code.Backend.Commands.save_recipe.get_supabase_client",
        return_value=mock_client,
    ):
        result, status = save_recipe(1, 1)

    assert status == 409
    assert result["error"] == "Recipe already saved"


def test_save_recipe_recipe_not_found_returns_404():
    mock_recipe_check = MagicMock()
    mock_recipe_check.data = None

    mock_client = MagicMock()
    mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_recipe_check

    with patch(
        "Source_Code.Backend.Commands.save_recipe.get_supabase_client",
        return_value=mock_client,
    ):
        result, status = save_recipe(1, 99)

    assert status == 404
    assert result["error"] == "Recipe not found"


def test_save_recipe_success_returns_success_dict():
    # Recipe exists
    mock_recipe_check = MagicMock()
    mock_recipe_check.data = [{"recipe_id": 1}]

    # Not already saved
    mock_existing = MagicMock()
    mock_existing.data = None

    # Insert succeeds
    mock_result = MagicMock()
    mock_result.data = [{"user_id": 1, "recipe_id": 1, "relation_type": "saved"}]

    mock_client = MagicMock()
    mock_client.table.side_effect = [
        # Recipe check
        MagicMock(select=MagicMock(return_value=MagicMock(eq=MagicMock(return_value=MagicMock(execute=MagicMock(return_value=mock_recipe_check)))))),
        # Existing check
        MagicMock(select=MagicMock(return_value=MagicMock(eq=MagicMock(return_value=MagicMock(eq=MagicMock(return_value=MagicMock(eq=MagicMock(return_value=MagicMock(execute=MagicMock(return_value=mock_existing)))))))))),
        # Insert
        MagicMock(insert=MagicMock(return_value=MagicMock(execute=MagicMock(return_value=mock_result)))),
    ]

    with patch(
        "Source_Code.Backend.Commands.save_recipe.get_supabase_client",
        return_value=mock_client,
    ):
        result = save_recipe(1, 1)

    assert result["success"] is True
    assert result["user_id"] == 1
    assert result["recipe_id"] == 1


def test_unsave_recipe_missing_user_or_recipe_returns_400():
    result, status = unsave_recipe(None, 1)
    assert status == 400
    assert result["error"] == "Missing user_id or recipe_id"

    result, status = unsave_recipe(1, None)
    assert status == 400
    assert result["error"] == "Missing user_id or recipe_id"


def test_unsave_recipe_success_returns_200():
    mock_result = MagicMock()
    mock_result.data = [{"user_id": 1, "recipe_id": 1, "relation_type": "saved"}]

    mock_client = MagicMock()
    mock_client.table.return_value.delete.return_value.eq.return_value.eq.return_value.eq.return_value.execute.return_value = mock_result

    with patch(
        "Source_Code.Backend.Commands.unsave_recipe.get_supabase_client",
        return_value=mock_client,
    ):
        result, status = unsave_recipe(1, 1)

    assert status == 200
    assert result["success"] is True
    assert result["user_id"] == 1
    assert result["recipe_id"] == 1


def test_unsave_recipe_exception_returns_500():
    mock_client = MagicMock()
    mock_client.table.return_value.delete.return_value.eq.return_value.eq.return_value.eq.return_value.execute.side_effect = Exception("DB error")

    with patch(
        "Source_Code.Backend.Commands.unsave_recipe.get_supabase_client",
        return_value=mock_client,
    ):
        result, status = unsave_recipe(1, 1)

    assert status == 500
    assert "DB error" in result["error"]


def test_add_pantry_item_missing_user_or_ingredient():
    # Missing user_id
    result, status = add_pantry_item(None, "Flour")
    assert status == 400
    assert "Missing user_id" in result["error"]

    # Missing ingredient_name
    result, status = add_pantry_item(1, None)
    assert status == 400
    assert "ingredient_name" in result["error"]


def test_add_pantry_item_existing_ingredient_updates():
    mock_client = MagicMock()
    # Existing ingredient found
    mock_client.table.return_value.select.return_value.ilike.return_value.execute.return_value.data = [{"ingredient_id": 10}]
    # Existing pantry item
    mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [{"ingredient_id": 10}]
    # Update returns
    mock_client.table.return_value.update.return_value.eq.return_value.eq.return_value.execute.return_value.data = [{"ingredient_id": 10}]

    with patch("Source_Code.Backend.Commands.add_pantry_item.get_supabase_client", return_value=mock_client):
        result, status = add_pantry_item(1, "Flour", 100, "g")

    assert status == 201
    assert result["ingredient_id"] == 10
    assert result["ingredient_name"] == "Flour"


def test_add_pantry_item_new_ingredient_inserts():
    mock_client = MagicMock()
    # No existing ingredient
    mock_client.table.return_value.select.return_value.ilike.return_value.execute.return_value.data = []
    # Insert new ingredient
    mock_client.table.return_value.insert.return_value.execute.return_value.data = [{"ingredient_id": 20}]
    # No existing pantry item
    mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
    # Insert pantry item
    mock_client.table.return_value.insert.return_value.execute.return_value.data = [{"ingredient_id": 20}]

    with patch("Source_Code.Backend.Commands.add_pantry_item.get_supabase_client", return_value=mock_client):
        result, status = add_pantry_item(1, "Sugar", 50, "g")

    assert status == 201
    assert result["ingredient_id"] == 20
    assert result["ingredient_name"] == "Sugar"


def test_add_pantry_item_exception_handling():
    mock_client = MagicMock()
    mock_client.table.side_effect = Exception("DB error")

    with patch("Source_Code.Backend.Commands.add_pantry_item.get_supabase_client", return_value=mock_client):
        result, status = add_pantry_item(1, "Salt")

    assert status == 500
    assert "DB error" in result["error"]


def test_remove_pantry_item_missing_user_or_ingredient():
    # Missing user_id
    result, status = remove_pantry_item(None, 10)
    assert status == 400
    assert "Missing" in result["error"]

    # Missing ingredient_id
    result, status = remove_pantry_item(1, None)
    assert status == 400
    assert "Missing" in result["error"]


def test_remove_pantry_item_successful_deletion():
    mock_client = MagicMock()
    # Delete chain
    mock_client.table.return_value.delete.return_value.eq.return_value.eq.return_value.execute.return_value.data = [{"ingredient_id": 10}]

    with patch("Source_Code.Backend.Commands.remove_pantry_item.get_supabase_client", return_value=mock_client):
        result, status = remove_pantry_item(1, 10)

    assert status == 200
    assert result["success"] is True
    assert result["user_id"] == 1
    assert result["ingredient_id"] == 10


def test_remove_pantry_item_exception_handling():
    mock_client = MagicMock()
    mock_client.table.side_effect = Exception("DB error")

    with patch("Source_Code.Backend.Commands.remove_pantry_item.get_supabase_client", return_value=mock_client):
        result, status = remove_pantry_item(1, 10)

    assert status == 500
    assert "DB error" in result["error"]
