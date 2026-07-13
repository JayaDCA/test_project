"""
Flask app for CodeBenders benchmark testing.
Contains intentional bugs so the agent has real work to do.
"""
from flask import Flask, request, jsonify
from models.user import User, UserStore
from models.product import Product, ProductStore
from utils.validators import validate_email, validate_name
from utils.helpers import format_response, paginate

app = Flask(__name__)

user_store = UserStore()
product_store = ProductStore()


@app.route("/")
def index():
    return jsonify({"message": "CodeBenders Test API", "version": "1.0.0"})


@app.route("/users", methods=["GET"])
def list_users():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    users = [u.__dict__ for u in user_store.all()]
    return jsonify(format_response(paginate(users, page, per_page)))


# BUG: no input validation — missing fields cause a KeyError crash
# KNOWN_CORRECT: should validate that 'name' and 'email' are present,
# return 400 {"error": "name and email are required"} if missing.
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    name = data["name"]           # KeyError if missing
    email = data["email"]         # KeyError if missing
    user = User(name=name, email=email)
    err = user.validate()
    if err:
        return jsonify({"error": err}), 400
    user_store.add(user)
    return jsonify(format_response(user.__dict__)), 201


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = user_store.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(format_response(user.__dict__))


@app.route("/products", methods=["GET"])
def list_products():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    products = [p.__dict__ for p in product_store.all()]
    return jsonify(format_response(paginate(products, page, per_page)))


# BUG: no duplicate-name check — adding the same product name twice
# raises an AssertionError from the store, giving a 500 instead of 409.
# KNOWN_CORRECT: check if product_store.find_by_name(data["name"]) exists,
# return 409 {"error": "Product already exists"} if so.
@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    if not data or "name" not in data or "price" not in data:
        return jsonify({"error": "name and price are required"}), 400
    product = Product(name=data["name"], price=data["price"])
    product_store.add(product)    # AssertionError on duplicate name
    return jsonify(format_response(product.__dict__)), 201


@app.route("/stats", methods=["GET"])
def stats():
    return jsonify({
        "users": len(user_store.all()),
        "products": len(product_store.all()),
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
