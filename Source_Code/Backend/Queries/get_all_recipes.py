from Supabase_client import supabase_connection

def get_all_recipes():
    """fetch_all_recipes"""

    response = supabase_connection.table("RECIPE").select("*").execute()

    return(response.data)