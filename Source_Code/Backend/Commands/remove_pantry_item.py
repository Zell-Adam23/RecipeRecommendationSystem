# remove_pantry_item.py - Command to remove item from user's pantry

from ..Supabase_client import get_supabase_client

supabase_connection = get_supabase_client()

def remove_pantry_item(user_id, ingredient_id):
    """Remove an ingredient from user's pantry"""
    if not user_id or not ingredient_id:
        return {"error": "Missing user_id or ingredient_id"}, 400

    try:
        # Delete the pantry item
        result = supabase_connection.table("USER_PANTRY_ITEM")\
            .delete()\
            .eq("user_id", user_id)\
            .eq("ingredient_id", ingredient_id)\
            .execute()

        return {"success": True, "user_id": user_id, "ingredient_id": ingredient_id}, 200

    except Exception as e:
        return {"error": str(e)}, 500
