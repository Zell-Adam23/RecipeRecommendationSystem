# Backend_connections.py

# This is where the backend (python) will communicate with the frontend

# flask is what i have used before but we can change it if need be
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/api/recipes", methods=["GET"])
def get_all_recipes():
    """fetch_all_recipes"""

    # SQL Request for all recipes

    return jsonify()


@app.route("/api/recipes", methods=["POST"])
def insert_recipe():
    """insert_recipe"""
    data = request.get_json()

    #SQL request for adding recipe to the database

    return jsonify(), 201

@app.route("/api/recipes/search", methods=["POST"])
def search_recipe():
    """search_recipe"""
    data = request.get_json()

    #SQL request for searching for recipe in database

    return jsonify(), 201

@app.route("/api/recipes/edit", methods=["POST"])
def add_person():
    """edit_recipe"""
    data = request.get_json()

    #SQL request for adding recipe to the database

    return jsonify(), 201

@app.route("/api/users/<int:id>", methods=["GET"])
def get_user_by_id(id):
    """fetch_user_by_id"""

    # SQL Request for user

    return jsonify()

@app.route("/api/users/authenticate", methods=["POST"])
def authenticate():
    """authenticate user"""

    data = request.get_json()

    # SQL Request for authenticating user

    return jsonify()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)