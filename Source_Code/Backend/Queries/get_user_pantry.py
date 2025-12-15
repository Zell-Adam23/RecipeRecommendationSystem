# get_user_pantry.py - Query to get user's pantry items

from ..Supabase_client import get_supabase_client


def get_user_pantry(user_id):
    """Get all pantry items for a user with ingredient details"""

    supabase_connection = get_supabase_client()

    if not user_id:
        return []

    try:
        # Get pantry items with ingredient names joined
        pantry_items = supabase_connection.table("USER_PANTRY_ITEM")\
            .select("ingredient_id, quantity, unit")\
            .eq("user_id", user_id)\
            .execute()

        if not pantry_items.data:
            return []

        # Enrich with ingredient names
        result = []
        for item in pantry_items.data:
            ingredient = supabase_connection.table("INGREDIENT")\
                .select("name")\
                .eq("ingredient_id", item["ingredient_id"])\
                .single()\
                .execute()

            result.append({
                "ingredient_id": item["ingredient_id"],
                "ingredient_name": ingredient.data["name"] if ingredient.data else "Unknown",
                "quantity": item["quantity"],
                "unit": item["unit"]
            })

        return result

    except Exception as e:
        print(f"Error fetching pantry: {e}")
        return []
