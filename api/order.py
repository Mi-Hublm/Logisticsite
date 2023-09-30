from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
from dotenv import load_dotenv


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

# Define the Order model for the database
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    delivery_address = db.Column(db.String(200), nullable=False)
    items = db.Column(db.String(500), nullable=False)

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

# Registration (No authentication required for registration)
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registration successful"}), 201

# Protected route example - requires a valid access token
@app.route("/api/orders", methods=["POST"])
@jwt_required()
def create_order():
    current_user = get_jwt_identity()
    data = request.get_json()
    customer_name = data.get("customer_name")
    delivery_address = data.get("delivery_address")
    items = data.get("items")

    if not customer_name or not delivery_address or not items:
        return jsonify({"message": "Customer name, delivery address, and items are required"}), 400

    new_order = Order(customer_name=customer_name, delivery_address=delivery_address, items=items)
    db.session.add(new_order)
    db.session.commit()

    return jsonify({"message": "Order created successfully", "order_id": new_order.id}), 201

# Modified DELETE route to allow users to delete their own orders
@app.route("/api/orders/<int:order_id>", methods=["DELETE"])
@jwt_required()
def cancel_order(order_id):
    current_user = get_jwt_identity()
    
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"message": "Order not found"}), 404

    # Check if the order belongs to the current user or if the user is an admin
    if current_user.get("is_admin") or current_user.get("username") == order.customer_name:
        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order canceled successfully"})
    else:
        return jsonify({"message": "Permission denied. You can only cancel your own orders or require admin access"}), 403


if __name__ == "__main__":
    app.run(debug=True)
