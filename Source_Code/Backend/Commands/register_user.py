from ..Supabase_client import get_supabase_client
from datetime import datetime, timezone
import bcrypt

def register_user(data):
    """Register a new user with hashed password"""

    email = data.get("email")
    password = data.get("password_hash")  # Frontend sends it as password_hash but it's plain text
    display_name = data.get("display_name")

    # Validate required fields
    if not email or not password or not display_name:
        return {"error": "Missing required fields"}, 400

    # Check if user already exists
    existing_user = get_supabase_client().table("USER_AUTH").select("email").eq("email", email).execute()
    if existing_user.data:
        return {"error": "Email already exists"}, 409

    # Hash the password
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    # Create user account first
    user_account = {
        "display_name": display_name,
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    user_response = get_supabase_client().table("USER_ACCOUNT").insert(user_account).execute()

    if not user_response.data:
        return {"error": "Failed to create user account"}, 500

    user_id = user_response.data[0]["user_id"]

    # Create auth record with hashed password
    user_auth = {
        "user_id": user_id,
        "email": email,
        "password_hash": hashed_password.decode('utf-8')  # Store as string in database
    }

    auth_response = get_supabase_client().table("USER_AUTH").insert(user_auth).execute()

    if not auth_response.data:
        # Rollback: delete the user account if auth creation fails
        get_supabase_client().table("USER_ACCOUNT").delete().eq("user_id", user_id).execute()
        return {"error": "Failed to create authentication record"}, 500

    # Return user info (same format as login)
    return {
        "user_id": user_id,
        "email": email,
        "display_name": display_name
    }
