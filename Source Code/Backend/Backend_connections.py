# Backend_connections.py

# This is where the api will communicate with the backend

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
def add_person():
    """insert_recipe"""
    data = request.get_json()

    #SQL request for adding recipe to the database

    return jsonify(), 201


@app.route("/api/check", methods=["GET"])
def quick_check():
    """check if working"""
    return jsonify({"status":"ok"}), 200



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)