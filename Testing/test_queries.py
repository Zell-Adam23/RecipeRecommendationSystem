import pytest
from unittest.mock import MagicMock, patch

from Source_Code.Backend.Queries.get_all_recipes import get_all_recipes
from Source_Code.Backend.Queries.get_full_recipe import get_recipe_by_id
from Source_Code.Backend.Queries.get_saved_recipes import get_saved_recipes
from Source_Code.Backend.Queries.get_user_by_id import get_user_by_id
from Source_Code.Backend.Queries.search_recipes import search_recipe
from Source_Code.Backend.Queries.get_user_pantry import get_user_pantry
from Source_Code.Backend.Queries.search_recipes_by_pantry import search_recipes_by_pantry



def test_get_all_recipes_returns_data():
    mock_response = MagicMock()
    mock_response.data = [
        {"recipe_id": 1, "name": "Spaghetti"},
        {"recipe_id": 2, "name": "Tacos"},
    ]

    mock_client = MagicMock()
    mock_client.table.return_value.select.return_value.execute.return_value = mock_response


    with patch(
        "Source_Code.Backend.Queries.get_all_recipes.get_supabase_client",
        return_value=mock_client,
    ):
        result = get_all_recipes()

    assert result == mock_response.data

def test_get_recipe_by_id_returns_none_when_not_found():
    mock_client = MagicMock()

    # RECIPE.single().execute().data returns None
    mock_client.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value.data = None

    with patch(
        "Source_Code.Backend.Queries.get_full_recipe.get_supabase_client",
        return_value=mock_client,
    ):
        result = get_recipe_by_id(999)

    assert result is None


def test_get_recipe_by_id_full():
    # --- Mock data ---
    mock_recipe = {"recipe_id": 1, "name": "Pasta"}
    mock_metadata = {"prep_time": 20}
    mock_cuisine_tags = [{"cuisine_id": 1}]
    mock_cuisines = [{"cuisine_id": 1, "name": "Italian"}]
    mock_diet_tags = [{"diet_tag_id": 2}]
    mock_diets = [{"diet_tag_id": 2, "name": "Vegetarian"}]
    mock_equipment_tags = [{"equipment_id": 3}]
    mock_equipment = [{"equipment_id": 3, "name": "Pot"}]
    mock_ingredient_tags = [{"ingredient_id": 4, "quantity": 100, "unit": "g", "optional": False}]
    mock_ingredients = [{"ingredient_id": 4, "name": "Flour"}]
    mock_ratings = [{"user_id": 10, "rating": 5}]

    # --- Helper to create a MagicMock that returns .data ---
    def mk_response(data):
        mock = MagicMock()
        mock.data = data
        return mock

    # --- Create a helper function to mock table.select().eq().single().execute() chain ---
    def mock_chain(return_data):
        execute_mock = MagicMock()
        execute_mock.data = return_data

        single_mock = MagicMock()
        single_mock.execute.return_value = execute_mock

        eq_mock = MagicMock()
        eq_mock.single.return_value = single_mock
        eq_mock.execute.return_value = execute_mock  # for non-single queries

        select_mock = MagicMock()
        select_mock.eq.return_value = eq_mock
        select_mock.in_.return_value.execute.return_value = mk_response(return_data)
        select_mock.execute.return_value = mk_response(return_data)

        table_mock = MagicMock()
        table_mock.select.return_value = select_mock

        return table_mock

    # --- Mock Supabase client ---
    mock_client = MagicMock()
    # Order of .table calls in get_recipe_by_id
    mock_client.table.side_effect = [
        mock_chain(mock_recipe),          # RECIPE
        mock_chain(mock_metadata),        # RECIPE_METADATA
        mock_chain(mock_cuisine_tags),    # RECIPE_CUISINE_TAG
        mock_chain(mock_cuisines),        # CUISINE_TAG
        mock_chain(mock_diet_tags),       # RECIPE_DIET_TAG
        mock_chain(mock_diets),           # DIET_TAG
        mock_chain(mock_equipment_tags),  # RECIPE_EQUIPMENT
        mock_chain(mock_equipment),       # EQUIPMENT
        mock_chain(mock_ingredient_tags), # RECIPE_INGREDIENT
        mock_chain(mock_ingredients),     # INGREDIENT
        mock_chain(mock_ratings),         # RECIPE_RATING
    ]

    # --- Patch the Supabase client and call function ---
    with patch(
        "Source_Code.Backend.Queries.get_full_recipe.get_supabase_client",
        return_value=mock_client
    ):
        result = get_recipe_by_id(1)

    # --- Assertions ---
    assert result["name"] == "Pasta"
    assert result["metadata"] == mock_metadata
    assert result["cuisine_tags"] == mock_cuisines
    assert result["diet_tags"] == mock_diets
    assert result["equipment"] == mock_equipment
    assert result["ingredients"] == [
        {
            "ingredient_id": 4,
            "name": "Flour",
            "quantity": 100,
            "unit": "g",
            "optional": False
        }
    ]
    assert result["ratings"] == mock_ratings


def test_get_saved_recipes_no_user_id_returns_empty_list():
    result = get_saved_recipes(None)
    assert result == []


def test_get_saved_recipes_returns_empty_when_no_saved_recipes():
    mock_response = MagicMock()
    mock_response.data = []

    mock_client = MagicMock()
    mock_client.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value = mock_response

    with patch(
        "Source_Code.Backend.Queries.get_saved_recipes.get_supabase_client",
        return_value=mock_client,
    ):
        result = get_saved_recipes(1)

    assert result == []


def test_get_saved_recipes_returns_saved_recipes():
    mock_response = MagicMock()
    mock_response.data = [
        {"recipe_id": 1},
        {"recipe_id": 2},
    ]

    mock_client = MagicMock()
    mock_client.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value = mock_response

    with patch(
        "Source_Code.Backend.Queries.get_saved_recipes.get_supabase_client",
        return_value=mock_client,
    ):
        result = get_saved_recipes(42)

    assert result == mock_response.data

def test_get_user_by_id_returns_user_data():
    mock_response = MagicMock()
    mock_response.data = {
        "user_id": 1,
        "display_name": "Adam",
        "email": "adam@example.com",
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
        "Source_Code.Backend.Queries.get_user_by_id.get_supabase_client",
        return_value=mock_client,
    ):
        result = get_user_by_id(1)

    assert result == mock_response.data


def test_search_recipe_returns_results():
    mock_response = MagicMock()
    mock_response.data = [
        {"recipe_id": 1, "title": "Chicken Soup"},
        {"recipe_id": 2, "title": "Chicken Alfredo"},
    ]

    mock_client = MagicMock()
    (
        mock_client.table.return_value
        .select.return_value
        .ilike.return_value
        .execute.return_value
    ) = mock_response

    with patch(
        "Source_Code.Backend.Queries.search_recipes.get_supabase_client",
        return_value=mock_client,
    ):
        result = search_recipe("chicken")

    assert result == mock_response.data

def test_get_user_pantry_basic():
    user_id = 1

    # Mock pantry items returned by Supabase
    mock_pantry_data = [{"ingredient_id": 10, "quantity": 100, "unit": "g"}]
    mock_ingredient_data = {"name": "Flour"}

    # Helper to mock .table().select().eq().single().execute()
    mock_execute = MagicMock()
    mock_execute.data = mock_ingredient_data

    mock_single = MagicMock()
    mock_single.execute.return_value = mock_execute

    mock_eq = MagicMock()
    mock_eq.single.return_value = mock_single
    mock_eq.execute.return_value = MagicMock(data=mock_pantry_data)

    mock_select = MagicMock()
    mock_select.eq.return_value = mock_eq
    mock_select.execute.return_value = MagicMock(data=mock_pantry_data)

    mock_table = MagicMock()
    mock_table.select.return_value = mock_select

    mock_client = MagicMock()
    mock_client.table.return_value = mock_table

    with patch("Source_Code.Backend.Queries.get_user_pantry.get_supabase_client", return_value=mock_client):
        result = get_user_pantry(user_id)

    assert result == [{
        "ingredient_id": 10,
        "ingredient_name": "Flour",
        "quantity": 100,
        "unit": "g"
    }]


def test_search_recipes_by_pantry_basic():
    user_id = 1

    # Mock data
    pantry_items = [{"ingredient_id": 10}]
    ingredient_lookup = {"name": "Flour"}
    recipes = [{"recipe_id": 1, "title": "Cake", "short_description": "Tasty"}]
    recipe_ingredients = [{"ingredient_id": 10, "quantity": 100, "unit": "g", "optional": False}]

    # Create a MagicMock client
    mock_client = MagicMock()

    # Function to return different data depending on table name
    def table_side_effect(table_name):
        table_mock = MagicMock()
        if table_name == "USER_PANTRY_ITEM":
            table_mock.select.return_value.eq.return_value.execute.return_value.data = pantry_items
        elif table_name == "INGREDIENT":
            table_mock.select.return_value.eq.return_value.single.return_value.execute.return_value.data = ingredient_lookup
        elif table_name == "RECIPE":
            table_mock.select.return_value.eq.return_value.execute.return_value.data = recipes
        elif table_name == "RECIPE_INGREDIENT":
            table_mock.select.return_value.eq.return_value.execute.return_value.data = recipe_ingredients
        else:
            table_mock.select.return_value.eq.return_value.execute.return_value.data = []
        return table_mock

    mock_client.table.side_effect = table_side_effect

    with patch("Source_Code.Backend.Queries.search_recipes_by_pantry.get_supabase_client", return_value=mock_client):
        result = search_recipes_by_pantry(user_id)

    # Assertions
    assert len(result) == 1
    assert result[0]["title"] == "Cake"
    assert result[0]["required_ingredients_count"] == 1
    assert result[0]["matched_ingredients_count"] == 1
    assert result[0]["match_percentage"] == 100.0
    ingredient = result[0]["ingredients"][0]
    assert ingredient["name"] == "Flour"
    assert ingredient["in_pantry"] is True
    assert ingredient["match_type"] == "exact"