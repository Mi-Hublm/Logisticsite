from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from api.shipments import Shipment
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SECRET_KEY")
db = SQLAlchemy(app)

# Define a Shipment model for the database (representing tracking data)
class Shipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100))

# Create the database tables (you would run this once to initialize your database)
with app.app_context():
    db.create_all()

@app.route("/api/tracking/<string:tracking_number>", methods=["GET"])
def track_shipment(tracking_number):
    shipment = Shipment.query.filter_by(tracking_number=tracking_number).first()

    if shipment:
        return jsonify({"tracking_number": shipment.tracking_number, "status": shipment.status, "location": shipment.location}), 200

    return jsonify({"message": "Tracking number not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
