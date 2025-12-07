from Supabase_client import supabase_connection

def get_user_by_id(id):
    """fetch_user_by_id"""

    response = supabase_connection.table("USER_ACCOUNT").select("*").eq("user_id", id).single().execute()

    return response.data