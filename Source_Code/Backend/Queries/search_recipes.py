from Supabase_client import get_supabase_client

def search_recipe(query):
    """search_recipe"""

    response = get_supabase_client().table("RECIPE").select("*").ilike("title", f"%{query}").execute()
    
    return (response.data)