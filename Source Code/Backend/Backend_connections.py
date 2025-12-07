# Backend_connections.py

# This is where the backend (python) will communicate with the frontend

# flask is what i have used before but we can change it if need be
from flask import Flask, jsonify, request
from flask_cors import CORS
from Supabase_client import supabase_connection
from datetime import datetime, timezone

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/api/recipes", methods=["GET"])
def get_all_recipes():
    """fetch_all_recipes"""

    response = supabase_connection.table("RECIPE").select("*").execute()
    
    return jsonify(response), 200


@app.route("/api/recipes", methods=["POST"])
def insert_recipe():
    """insert_recipe"""
    data = request.get_json()

    recipe = {
        "title": data.get("title"),
        "short_description": data.get("short_description"),
        "is_public": data.get("is_public", True),
        "created_at": datetime.now(timezone.utc)
    }

    response = supabase_connection.table("RECIPE").insert(recipe).execute()
    return jsonify(response.data), 201

@app.route("/api/recipes/search", methods=["POST"])
def search_recipe():
    """search_recipe"""
    data = request.get_json()
    query = data.get("query", "")

    response = supabase_connection.table("RECIPE").select("*").ilike("title", f"%{query}").execute()
    return jsonify(response.data), 200

@app.route("/api/recipes/edit", methods=["POST"])
def edit_recipe():
    """edit_recipe"""
    data = request.get_json()
    recipe_id = data.get("recipe_id")

    update_fields = {x: y for x, y in data.items() if x != "recipe_id"}
    
    response=supabase_connection.table("RECIPE").update(update_fields).eq("recipe_id", recipe_id).execute()

    return jsonify(response.data), 200

@app.route("/api/users/<int:id>", methods=["GET"])
def get_user_by_id(id):
    """fetch_user_by_id"""

    response = supabase_connection.table("USER_ACCOUNT").select("*").eq("user_id", id).single().execute()

    return jsonify(response.data), 200

@app.route("/api/users/authenticate", methods=["POST"])
def authenticate():
    """authenticate user"""

    data = request.get_json()
    email = data.get("email")
    password = data.get("password_hash")

    user = supabase_connection.table("USER_AUTH").select("user_id, email, password_hash").eq("email", email).single().execute()

    if not user.data:
        return jsonify({"error": "Invalid email"}), 404
    if user.data["password_hash"] != password:
        return jsonify({"error": "invalid password"}), 401
    return jsonify({"user_id": user.data["user_id"], "email": email}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)