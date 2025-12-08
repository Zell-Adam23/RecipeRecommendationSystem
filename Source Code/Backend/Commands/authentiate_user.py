from Supabase_client import supabase_connection
import bcrypt

def authenticate(email, password):
    """authenticate user"""

    try:
        user = supabase_connection.table("USER_AUTH").select("user_id, email, password_hash").eq("email", email).single().execute()

        if not user.data:
            return None

        # Get the stored hashed password
        stored_hash = user.data["password_hash"]

        # Convert password to bytes
        password_bytes = password.encode('utf-8')
        stored_hash_bytes = stored_hash.encode('utf-8')

        # Verify the password against the hash
        if bcrypt.checkpw(password_bytes, stored_hash_bytes):
            return user.data["user_id"]
        else:
            return None

    except Exception as e:
        print(f"Authentication error: {e}")
        return None