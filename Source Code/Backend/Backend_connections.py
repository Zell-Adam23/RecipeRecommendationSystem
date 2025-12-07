# Backend_connections.py

# This is where the backend (python) will communicate with the frontend

"""
api/recipes, GET: returns all entries from RECIPE table
api/recipes, POST: adds a recipe to the database
api/recipes/<int:recipe_id>, GET: returns a specifc recipe with all included metadata, cuisine tags, diet_tags, equipment, ingredients, and ratings
api/recipes/search, POST: searches for a recipe (at the moment, just in the recipe table)
api/recipes/edit, POST: edits an existing recipe
api/users/<int:id>, GET: fetches inofrmation of a particular user
api/users/authenticate, POST:authenticates a users password
"""

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
    
    return jsonify(response.data), 200


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

@app.route("/api/recipes/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):

    #fetch recipe
    recipe = (supabase_connection.table("RECIPE").select("*").eq("recipe_id", recipe_id).single().execute()).data
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404
    
    #fetch metadata
    metadata = (supabase_connection.table("RECIPE_METADATA").select("*").eq("recipe_id", recipe_id).single().execute()).data
    recipe["metadata"] = metadata

    #fetch cuisine
    cuisine_tags = (supabase_connection.table("RECIPE_CUISINE_TAG").select("cuisine_id").eq("recipe_id", recipe_id).execute())
    cuisine_ids = [x["cuisine_id"] for x in cuisine_tags]

    if cuisine_ids:
        cuisines = (supabase_connection.table("CUISINE_TAG").select("*").in_("cuisine_id", cuisine_ids).execute()).data
    else:
        cuisines = []
    
    recipe["cuisine_tags"] = cuisines

    #fetch diet
    diet_tags = (supabase_connection.table("RECIPE_DIET_TAG").select("diet_id").eq("recipe_id", recipe_id).execute()).data
    diet_ids = [x["diet_tag_id"] for x in diet_tags]

    if diet_ids:
        diets = (supabase_connection.table("DIET_TAG").select("*").in_("diet_tag_id", diet_ids).execute()).data
    else:
        diets = []

    recipe["diet_tags"] = diets

    #fetch equipment
    equipment_tags = (supabase_connection.table("RECIPE_EQUIPMENT").select("equipment_id").eq("recipe_id", recipe_id).execute()).data
    equipment_ids = [x["recipe_id"] for x in equipment_tags]

    if equipment_ids:
        equipment = (supabase_connection.table("EQUIPMENT").select("*").in_("equipment_id", equipment_ids).execute()).data
    else:
        equipment = []

    recipe["equipment"] = equipment

    #fetch ingredients
    ingredient_tags = (supabase_connection.table("RECIPE_INGREDIENTS").select("*").eq("recipe_id", recipe_id).execute()).data
    ingredient_ids = [x["ingredient_id"] for x in ingredient_tags]

    if ingredient_ids:
        ingredients = (supabase_connection.table("INGREDIENT").select("*").in_("ingredient_id", ingredient_ids).execute()).data
    else:
        ingredients = []

    ingredients_with_quantities = []
    for current in ingredient_tags:
        x = next((y for y in ingredients if y["ingredient_id"] == current["ingredient_id"]), None)
        ingredients_with_quantities.append({
            "ingredient_id": current["ingredient_id"],
            "name": x["name"],
            "quantity": current["quantity"],
            "unit": current["unit"],
            "optional": current["optional"]
        })

    recipe["ingredients"] = ingredients_with_quantities

    #fetch ratings
    ratings = (supabase_connection.table("RECIPE_RATING").select("*").eq("recipe_id").execute()).data

    recipe["ratings"] = ratings

    return jsonify(recipe), 200

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