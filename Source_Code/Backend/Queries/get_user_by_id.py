from ..Supabase_client import get_supabase_client

def get_user_by_id(id):
    """fetch_user_by_id"""

    response = get_supabase_client().table("USER_ACCOUNT").select("*").eq("user_id", id).single().execute()

    return response.data