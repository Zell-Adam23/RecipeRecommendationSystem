# main.py

# this file will be responisble for launching/managing the database
from supabase import create_client
from dotenv import load_dotenv
import os

def main():
    load_dotenv()


    supabase_url = os.getenv("SUPABASE_URL")
    supabase_service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not supabase_url or not supabase_service_key:
        print("invalid keys")
    
    connection = create_client(supabase_url, supabase_service_key)

    response = connection.table("recipes").select("*").execute()
    print (response.data)

if __name__ == "__main__":
    main()