# add_pantry_item.py - Command to add item to user's pantry

from Supabase_client import get_supabase_client


def add_pantry_item(user_id, ingredient_name, quantity=None, unit=None):
    """Add or update an ingredient in user's pantry"""
    if not user_id or not ingredient_name:
        return {"error": "Missing user_id or ingredient_name"}, 400

    supabase_connection = get_supabase_client()

    try:
        # Get or create ingredient
        ingredient = supabase_connection.table("INGREDIENT")\
            .select("ingredient_id")\
            .ilike("name", ingredient_name)\
            .execute()

        if ingredient.data and len(ingredient.data) > 0:
            ingredient_id = ingredient.data[0]["ingredient_id"]
        else:
            # Create new ingredient
            new_ingredient = supabase_connection.table("INGREDIENT")\
                .insert({"name": ingredient_name})\
                .execute()
            ingredient_id = new_ingredient.data[0]["ingredient_id"]

        # Check if pantry item already exists
        existing = supabase_connection.table("USER_PANTRY_ITEM")\
            .select("*")\
            .eq("user_id", user_id)\
            .eq("ingredient_id", ingredient_id)\
            .execute()

        pantry_data = {
            "user_id": user_id,
            "ingredient_id": ingredient_id,
            "quantity": quantity,
            "unit": unit
        }

        if existing.data and len(existing.data) > 0:
            # Update existing item
            result = supabase_connection.table("USER_PANTRY_ITEM")\
                .update({"quantity": quantity, "unit": unit})\
                .eq("user_id", user_id)\
                .eq("ingredient_id", ingredient_id)\
                .execute()
        else:
            # Insert new item
            result = supabase_connection.table("USER_PANTRY_ITEM")\
                .insert(pantry_data)\
                .execute()

        return {
            "success": True,
            "ingredient_id": ingredient_id,
            "ingredient_name": ingredient_name
        }, 201

    except Exception as e:
        return {"error": str(e)}, 500
