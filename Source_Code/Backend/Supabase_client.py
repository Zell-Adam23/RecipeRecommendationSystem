#Supabase_client

from supabase import create_client
import os

_supabase_connection = None

def get_supabase_client():
    global _supabase_connection

    if _supabase_connection is None:
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        if not supabase_url or not supabase_service_key:
            print("invalid keys")
        
        _supabase_connection = create_client(supabase_url, supabase_service_key)

    return _supabase_connection
