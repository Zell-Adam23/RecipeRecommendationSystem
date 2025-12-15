from ..Supabase_client import get_supabase_client

def get_all_recipes():
    """fetch_all_recipes"""

    response = get_supabase_client().table("RECIPE").select("*").execute()

    return(response.data)