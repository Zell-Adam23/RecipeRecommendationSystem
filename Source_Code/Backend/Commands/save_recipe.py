from ..Supabase_client import get_supabase_client

def save_recipe(user_id, recipe_id):
    """Save a recipe to user's saved list using USER_RECIPE_REL table"""

    if not user_id or not recipe_id:
        return {"error": "Missing user_id or recipe_id"}, 400

    # Check if recipe exists
    recipe_check = get_supabase_client().table("RECIPE").select("recipe_id").eq("recipe_id", recipe_id).execute()
    if not recipe_check.data:
        return {"error": "Recipe not found"}, 404

    # Check if already saved
    existing = get_supabase_client().table("USER_RECIPE_REL").select("*").eq("user_id", user_id).eq("recipe_id", recipe_id).eq("relation_type", "saved").execute()
    if existing.data:
        return {"error": "Recipe already saved"}, 409

    # Save the recipe
    save_data = {
        "user_id": user_id,
        "recipe_id": recipe_id,
        "relation_type": "saved"
    }

    result = get_supabase_client().table("USER_RECIPE_REL").insert(save_data).execute()

    if not result.data:
        return {"error": "Failed to save recipe"}, 500

    return {
        "success": True,
        "user_id": user_id,
        "recipe_id": recipe_id
    }
