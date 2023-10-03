from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI") # Use a proper database in production
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")  # Change this to a strong, random value in production
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


# Define the Route model for the database
class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    schedule = db.Column(db.String(500))
    # Add more route attributes as needed

# Create the database tables
with app.app_context():
    db.create_all()


# Routes and Schedules
@app.route("/api/routes", methods=["GET"])
@jwt_required()
def get_routes():
    current_user = get_jwt_identity()
    if not current_user.get("is_admin"):
        return jsonify({"message": "Permission denied. Admin access required"}), 403

    routes = Route.query.all()
    route_list = [{"id": route.id, "name": route.name, "schedule": route.schedule} for route in routes]
    return jsonify(route_list)

@app.route("/api/routes/<int:route_id>", methods=["GET"])
@jwt_required()
def get_route(route_id):
    current_user = get_jwt_identity()
    if not current_user.get("is_admin"):
        return jsonify({"message": "Permission denied. Admin access required"}), 403

    route = Route.query.get(route_id)
    if route:
        return jsonify({"id": route.id, "name": route.name, "schedule": route.schedule})
    return jsonify({"message": "Route not found"}), 404

@app.route("/api/routes", methods=["POST"])
@jwt_required()
def create_route():
    current_user = get_jwt_identity()
    if not current_user.get("is_admin"):
        return jsonify({"message": "Permission denied. Admin access required"}), 403

    data = request.get_json()
    name = data.get("name")
    schedule = data.get("schedule")

    if not name:
        return jsonify({"message": "Route name is required"}), 400

    new_route = Route(name=name, schedule=schedule)
    db.session.add(new_route)
    db.session.commit()

    return jsonify({"message": "Route created successfully", "route_id": new_route.id}), 201

@app.route("/api/routes/<int:route_id>", methods=["PUT"])
@jwt_required()
def update_route(route_id):
    current_user = get_jwt_identity()
    if not current_user.get("is_admin"):
        return jsonify({"message": "Permission denied. Admin access required"}), 403

    route = Route.query.get(route_id)

    if not route:
        return jsonify({"message": "Route not found"}), 404

    data = request.get_json()
    new_name = data.get("name")
    new_schedule = data.get("schedule")

    if new_name:
        route.name = new_name

    if new_schedule:
        route.schedule = new_schedule

    db.session.commit()

    return jsonify({"message": "Route updated successfully"})

@app.route("/api/routes/<int:route_id>", methods=["DELETE"])
@jwt_required()
def remove_route(route_id):
    current_user = get_jwt_identity()
    if not current_user.get("is_admin"):
        return jsonify({"message": "Permission denied. Admin access required"}), 403

    route = Route.query.get(route_id)

    if not route:
        return jsonify({"message": "Route not found"}), 404

    db.session.delete(route)
    db.session.commit()

    return jsonify({"message": "Route removed successfully"})

if __name__ == "__main__":
    app.run(debug=True)
