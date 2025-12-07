from Supabase_client import supabase_connection

def authenticate(email, password):
    """authenticate user"""

    user = supabase_connection.table("USER_AUTH").select("user_id, email, password_hash").eq("email", email).single().execute()

    if not user:
        return None
    if user.data["password_hash"] != password:
        return None
    return user.data["user_id"]