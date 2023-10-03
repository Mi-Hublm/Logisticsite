from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")  # Change this to a strong, random value in production
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Define the User model for the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

# Define the Product model for the database
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    price = db.Column(db.Float, nullable=False)
    # Add more product attributes as needed

# Create the database tables
with app.app_context():
    db.create_all()

# Authentication and authorization
@app.route("/api/authenticate", methods=["POST"])
def authenticate():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity={"username": username, "is_admin": user.is_admin})
        return jsonify({"message": "Authentication successful", "access_token": access_token}), 200

    return jsonify({"message": "Authentication failed"}), 401

# Inventory
@app.route("/api/inventory", methods=["GET"])
@jwt_required()
def get_inventory():
    current_user = get_jwt_identity()
    if not current_user.get("is_admin"):
        return jsonify({"message": "Permission denied. Admin access required"}), 403

    products = Product.query.all()
    product_list = [{"id": product.id, "name": product.name, "description": product.description, "price": product.price}
                    for product in products]
    return jsonify(product_list)

@app.route("/api/inventory/<int:product_id>", methods=["GET"])
@jwt_required()
def get_product(product_id):
    current_user = get_jwt_identity()
    if not current_user.get("is_admin"):
        return jsonify({"message": "Permission denied. Admin access required"}), 403

    product = Product.query.get(product_id)
    if product:
        return jsonify({"id": product.id, "name": product.name, "description": product.description, "price": product.price})
    return jsonify({"message": "Product not found"}), 404

@app.route("/api/inventory", methods=["POST"])
@jwt_required()
def add_product():
    current_user = get_jwt_identity()
    if not current_user.get("is_admin"):
        return jsonify({"message": "Permission denied. Admin access required"}), 403

    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    price = data.get("price")

    if not name or not price:
        return jsonify({"message": "Product name and price are required"}), 400

    new_product = Product(name=name, description=description, price=price)
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product added to inventory", "product_id": new_product.id}), 201

@app.route("/api/inventory/<int:product_id>", methods=["PUT"])
@jwt_required()
def update_product(product_id):
    current_user = get_jwt_identity()
    if not current_user.get("is_admin"):
        return jsonify({"message": "Permission denied. Admin access required"}), 403

    product = Product.query.get(product_id)

    if not product:
        return jsonify({"message": "Product not found"}), 404

    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    price = data.get("price")

    if name:
        product.name = name

    if description:
        product.description = description

    if price:
        product.price = price

    db.session.commit()

    return jsonify({"message": "Product updated successfully"})

@app.route("/api/inventory/<int:product_id>", methods=["DELETE"])
@jwt_required()
def remove_product(product_id):
    current_user = get_jwt_identity()
    if not current_user.get("is_admin"):
        return jsonify({"message": "Permission denied. Admin access required"}), 403

    product = Product.query.get(product_id)

    if not product:
        return jsonify({"message": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product removed from inventory"})

if __name__ == "__main__":
    app.run(debug=True)
