from Supabase_client import supabase_connection
from datetime import datetime, timezone

def insert_recipe(data):
    """insert_recipe"""
    
    recipe = {
        "title": data.get("title"),
        "short_description": data.get("short_description"),
        "is_public": data.get("is_public", True),
        "created_at": datetime.now(timezone.cst)
    }

    response = supabase_connection.table("RECIPE").insert(recipe).execute()
    return (response.data)