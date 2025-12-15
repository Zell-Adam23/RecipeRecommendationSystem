from Supabase_client import supabase_connection

def search_recipe(query):
    """search_recipe"""

    response = supabase_connection.table("RECIPE").select("*").ilike("title", f"%{query}").execute()
    
    return (response.data)