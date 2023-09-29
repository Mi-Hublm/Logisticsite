from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use a proper database in production
db = SQLAlchemy(app)

# Define the Shipment model for the database
class Shipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)
    tracking_info = db.Column(db.String(200))
    # Add more shipment attributes as needed

# Create the database tables
db.create_all()

# Shipments
@app.route("/api/shipments", methods=["GET"])
def get_shipments():
    shipments = Shipment.query.all()
    shipment_list = [{"id": shipment.id, "status": shipment.status, "tracking_info": shipment.tracking_info}
                     for shipment in shipments]
    return jsonify(shipment_list)

@app.route("/api/shipments/<int:shipment_id>", methods=["GET"])
def get_shipment(shipment_id):
    shipment = Shipment.query.get(shipment_id)
    if shipment:
        return jsonify({"id": shipment.id, "status": shipment.status, "tracking_info": shipment.tracking_info})
    return jsonify({"message": "Shipment not found"}), 404

# Create a new shipment
@app.route("/api/shipments", methods=["POST"])
def create_shipment():
    data = request.get_json()
    status = data.get("status")
    tracking_info = data.get("tracking_info")

    if not status:
        return jsonify({"message": "Status is required"}), 400

    new_shipment = Shipment(status=status, tracking_info=tracking_info)
    db.session.add(new_shipment)
    db.session.commit()

    return jsonify({"message": "Shipment created successfully", "shipment_id": new_shipment.id}), 201

# Update shipment details
@app.route("/api/shipments/<int:shipment_id>", methods=["PUT"])
def update_shipment(shipment_id):
    shipment = Shipment.query.get(shipment_id)

    if not shipment:
        return jsonify({"message": "Shipment not found"}), 404

    data = request.get_json()
    status = data.get("status")
    tracking_info = data.get("tracking_info")

    if status:
        shipment.status = status

    if tracking_info:
        shipment.tracking_info = tracking_info

    db.session.commit()

    return jsonify({"message": "Shipment updated successfully"})

# Delete a shipment
@app.route("/api/shipments/<int:shipment_id>", methods=["DELETE"])
def delete_shipment(shipment_id):
    shipment = Shipment.query.get(shipment_id)

    if not shipment:
        return jsonify({"message": "Shipment not found"}), 404

    db.session.delete(shipment)
    db.session.commit()

    return jsonify({"message": "Shipment deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)
