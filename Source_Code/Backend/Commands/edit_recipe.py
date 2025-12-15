from Supabase_client import supabase_connection

def edit_recipe(recipe_id, update_fields):
    """edit_recipe"""
    
    response=supabase_connection.table("RECIPE").update(update_fields).eq("recipe_id", recipe_id).execute()

    return response.data