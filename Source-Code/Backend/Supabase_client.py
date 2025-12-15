#Supabase_client

from supabase import create_client
import os

supabase_url = os.environ.get("SUPABASE_URL")
supabase_service_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not supabase_url or not supabase_service_key:
    print("invalid keys")

supabase_connection = create_client(supabase_url, supabase_service_key)