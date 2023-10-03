from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
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

# Users
@app.route("/api/users", methods=["GET"])
@jwt_required()
def get_users():
    current_user = get_jwt_identity()
    if not current_user.get("is_admin"):
        return jsonify({"message": "Permission denied. Admin access required"}), 403

    users = User.query.all()
    user_list = [{"id": user.id, "username": user.username} for user in users]
    return jsonify(user_list)

@app.route("/api/users/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    current_user = get_jwt_identity()
    if not current_user.get("is_admin"):
        return jsonify({"message": "Permission denied. Admin access required"}), 403

    user = User.query.get(user_id)
    if user:
        return jsonify({"id": user.id, "username": user.username, "is_admin": user.is_admin})
    return jsonify({"message": "User not found"}), 404

@app.route("/api/users", methods=["POST"])
@jwt_required()
def create_user():
    current_user = get_jwt_identity()
    if not current_user.get("is_admin"):
        return jsonify({"message": "Permission denied. Admin access required"}), 403

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

    return jsonify({"message": "User created successfully"}), 201

@app.route("/api/users/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
    current_user = get_jwt_identity()
    if not current_user.get("is_admin"):
        return jsonify({"message": "Permission denied. Admin access required"}), 403

    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    new_username = data.get("username")

    if new_username:
        user.username = new_username

    db.session.commit()

    return jsonify({"message": "User updated successfully"})

@app.route("/api/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
def remove_user(user_id):
    current_user = get_jwt_identity()
    if not current_user.get("is_admin"):
        return jsonify({"message": "Permission denied. Admin access required"}), 403

    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User removed successfully"})

if __name__ == "__main__":
    app.run(debug=True)
