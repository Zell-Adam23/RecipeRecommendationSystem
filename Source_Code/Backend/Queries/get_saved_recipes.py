from Supabase_client import get_supabase_client

def get_saved_recipes(user_id):
    """Get all saved recipes for a user"""

    if not user_id:
        return []

    # Get all saved recipe relationships for this user
    saved = get_supabase_client().table("USER_RECIPE_REL").select("recipe_id").eq("user_id", user_id).eq("relation_type", "saved").execute()

    if not saved.data:
        return []

    return saved.data
