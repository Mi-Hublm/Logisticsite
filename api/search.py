from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from api.shipments import Shipment
from api.order import Order
from api.inventory import Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use your production database
db = SQLAlchemy(app)

# Define the Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_name = db.Column(db.String(100), nullable=False)
    order_date = db.Column(db.Date, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    # Add more order-related fields as needed

# Define the Shipment model
class Shipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String(50), nullable=False)
    shipment_date = db.Column(db.Date, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)

# Define the Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    # Add more product-related fields as needed

# Define the Customer model (used as a foreign key in the Order model)
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    # Add more customer-related fields as needed




# Search endpoint
@app.route("/api/search", methods=["GET"])
def search():
    query = request.args.get("query")  # Get the search query from the request parameters
    if not query:
        return jsonify({"message": "Query parameter 'query' is required"}), 400

    # Search in orders, shipments, and products based on your criteria
    orders = Order.query.filter(Order.order_name.ilike(f"%{query}%")).all()
    shipments = Shipment.query.filter(Shipment.tracking_number.ilike(f"%{query}%")).all()
    products = Product.query.filter(Product.product_name.ilike(f"%{query}%")).all()

    # Format the search results as needed
    order_results = [{"id": order.id, "order_name": order.order_name} for order in orders]
    shipment_results = [{"id": shipment.id, "tracking_number": shipment.tracking_number} for shipment in shipments]
    product_results = [{"id": product.id, "product_name": product.product_name} for product in products]

    # Create a response containing the search results
    search_results = {
        "orders": order_results,
        "shipments": shipment_results,
        "products": product_results,
    }

    return jsonify(search_results)

if __name__ == "__main__":
    app.run(debug=True)
