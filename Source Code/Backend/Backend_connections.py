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

from Queries.get_all_recipes import get_all_recipes
from Queries.get_full_recipe import get_recipe_by_id
from Queries.search_recipes import search_recipe
from Queries.get_user_by_id import get_user_by_id
from Commands.create_recipe import insert_recipe
from Commands.edit_recipe import edit_recipe
from Commands.authentiate_user import authenticate

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

@app.route("/api/users/<int:id>", methods=["GET"])
def api_get_user_by_id(id):
    """fetch_user_by_id"""

    return jsonify(get_user_by_id(id)), 200


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



@app.route("/api/users/authenticate", methods=["POST"])
def api_authenticate():
    """authenticate user"""

    data = request.get_json()
    email = data.get("email")
    password = data.get("password_hash")
    user_id = authenticate(email, password)


    if user_id is None:
        return jsonify({"error": "invalid credentials"}), 401
    return jsonify({"user_id": user_id}), 200



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)