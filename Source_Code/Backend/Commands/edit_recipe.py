from Supabase_client import get_supabase_client

def edit_recipe(recipe_id, update_fields):
    """edit_recipe"""
    
    response=get_supabase_client().table("RECIPE").update(update_fields).eq("recipe_id", recipe_id).execute()

    return response.data