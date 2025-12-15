# Backend_connections.py

# This is where the backend (python) will communicate with the frontend

"""
api/recipes, GET: returns all entries from RECIPE table
api/recipes, POST: adds a recipe to the database
api/recipes/<int:recipe_id>, GET: returns a specifc recipe with all included metadata, cuisine tags, diet_tags, equipment, ingredients, and ratings
api/recipes/search, POST: searches for a recipe (at the moment, just in the recipe table)
api/recipes/edit, POST: edits an existing recipe
api/users, POST: registers a new user with hashed password
api/users/<int:id>, GET: fetches inofrmation of a particular user
api/users/authenticate, POST: authenticates a users password (verifies hashed password)
"""

# flask is what i have used before but we can change it if need be
from flask import Flask, jsonify, request
from flask_cors import CORS

from .Supabase_client import get_supabase_client
from .Queries.get_all_recipes import get_all_recipes
from .Queries.get_full_recipe import get_recipe_by_id
from .Queries.search_recipes import search_recipe
from .Queries.get_user_by_id import get_user_by_id
from .Queries.get_saved_recipes import get_saved_recipes
from .Queries.get_user_pantry import get_user_pantry
from .Queries.search_recipes_by_pantry import search_recipes_by_pantry
from .Commands.create_recipe import insert_recipe
from .Commands.edit_recipe import edit_recipe
from .Commands.authentiate_user import authenticate
from .Commands.register_user import register_user
from .Commands.save_recipe import save_recipe
from .Commands.unsave_recipe import unsave_recipe
<<<<<<< HEAD
=======
from .Commands.add_pantry_item import add_pantry_item
from .Commands.remove_pantry_item import remove_pantry_item
>>>>>>> origin/main

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})

#---QUERIES---
@app.route("/api/recipes", methods=["GET"])
def api_get_all_recipes():
    """fetch_all_recipes"""
    
    return jsonify(get_all_recipes()), 200

@app.route("/api/recipes/<int:recipe_id>", methods=["GET"])
def api_get_recipe(recipe_id):
    recipe = get_recipe_by_id(recipe_id)
    if recipe is None:
        return jsonify({"error": "Recipe Not Found"}), 404
    return jsonify(recipe), 200

@app.route("/api/recipes/search", methods=["POST"])
def api_search_recipe():
    """search_recipe"""
    data = request.get_json()
    query = data.get("query", "")

    return jsonify(search_recipe(query)), 200

@app.route("/api/recipes/search-by-pantry/<int:user_id>", methods=["GET"])
def api_search_recipes_by_pantry(user_id):
    """search recipes by user's pantry ingredients"""

    return jsonify(search_recipes_by_pantry(user_id)), 200

@app.route("/api/users/<int:id>", methods=["GET"])
def api_get_user_by_id(id):
    """fetch_user_by_id"""

    return jsonify(get_user_by_id(id)), 200


@app.route("/api/saved-recipes/<int:user_id>", methods=["GET"])
def api_get_saved_recipes(user_id):
    """get all saved recipes for a user"""

    return jsonify(get_saved_recipes(user_id)), 200



#---COMMANDS---
@app.route("/api/recipes", methods=["POST"])
def api_insert_recipe():
    """insert_recipe"""

    data = request.get_json()

    return jsonify(insert_recipe(data)), 201


@app.route("/api/recipes/edit", methods=["POST"])
def api_edit_recipe():
    """edit_recipe"""
    data = request.get_json()
    recipe_id = data.get("recipe_id")

    update_fields = {x: y for x, y in data.items() if x != "recipe_id"}
    
    return jsonify(edit_recipe(recipe_id, update_fields)), 200


@app.route("/api/users", methods=["POST"])
def api_register_user():
    """register new user"""

    data = request.get_json()
    result = register_user(data)

    # Check if result is a tuple (error case)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify(result), 201


@app.route("/api/users/authenticate", methods=["POST"])
def api_authenticate():
    """authenticate user"""

    data = request.get_json()
    email = data.get("email")
    password = data.get("password_hash")
    user_id = authenticate(email, password)

    if user_id is None:
        return jsonify({"error": "invalid credentials"}), 401

    # Get user details to return (like registration does)
    user_data = get_supabase_client().table("USER_ACCOUNT").select("user_id, display_name").eq("user_id", user_id).single().execute()
    user_auth = get_supabase_client().table("USER_AUTH").select("email").eq("user_id", user_id).single().execute()

    return jsonify({
        "user_id": user_id,
        "display_name": user_data.data.get("display_name"),
        "email": user_auth.data.get("email")
    }), 200


@app.route("/api/saved-recipes", methods=["POST"])
def api_save_recipe():
    """save a recipe to user's saved list"""

    data = request.get_json()
    user_id = data.get("user_id")
    recipe_id = data.get("recipe_id")

    result = save_recipe(user_id, recipe_id)

    # Check if result is a tuple (error case)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify(result), 201


@app.route("/api/saved-recipes", methods=["DELETE"])
def api_unsave_recipe():
    """remove a recipe from user's saved list"""

    data = request.get_json()
    user_id = data.get("user_id")
    recipe_id = data.get("recipe_id")

    result = unsave_recipe(user_id, recipe_id)

    # Check if result is a tuple (error case)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify(result), 200


@app.route("/api/pantry/<int:user_id>", methods=["GET"])
def api_get_user_pantry(user_id):
    """get all pantry items for a user"""

    return jsonify(get_user_pantry(user_id)), 200


@app.route("/api/pantry", methods=["POST"])
def api_add_pantry_item():
    """add an item to user's pantry"""

    data = request.get_json()
    user_id = data.get("user_id")
    ingredient_name = data.get("ingredient_name")
    quantity = data.get("quantity")
    unit = data.get("unit")

    result = add_pantry_item(user_id, ingredient_name, quantity, unit)

    # Check if result is a tuple (error case)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify(result), 201


@app.route("/api/pantry", methods=["DELETE"])
def api_remove_pantry_item():
    """remove an item from user's pantry"""

    data = request.get_json()
    user_id = data.get("user_id")
    ingredient_id = data.get("ingredient_id")

    result = remove_pantry_item(user_id, ingredient_id)

    # Check if result is a tuple (error case)
    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify(result), 200



if __name__ == "__main__": #pragma: no cover
    app.run(debug=True)