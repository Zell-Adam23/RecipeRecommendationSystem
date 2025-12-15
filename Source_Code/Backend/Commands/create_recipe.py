from ..Supabase_client import get_supabase_client
from datetime import datetime, timezone

def insert_recipe(data):
    """insert_recipe"""

    recipe = {
        "title": data.get("title"),
        "short_description": data.get("short_description"),
        "is_public": data.get("is_public", True),
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    response = get_supabase_client().table("RECIPE").insert(recipe).execute()

    if response.data:
        return response.data[0]
    return None