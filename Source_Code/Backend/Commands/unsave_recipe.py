# unsave_recipe.py - Command to remove a saved recipe

from ..Supabase_client import get_supabase_client

def unsave_recipe(user_id, recipe_id):
    """Remove a recipe from user's saved list"""
    if not user_id or not recipe_id:
        return {"error": "Missing user_id or recipe_id"}, 400

    try:
        # Delete the saved recipe entry from USER_RECIPE_REL table
        result = get_supabase_client().table("USER_RECIPE_REL")\
            .delete()\
            .eq("user_id", user_id)\
            .eq("recipe_id", recipe_id)\
            .eq("relation_type", "saved")\
            .execute()

        return {"success": True, "user_id": user_id, "recipe_id": recipe_id}, 200

    except Exception as e:
        return {"error": str(e)}, 500
