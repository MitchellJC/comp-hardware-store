"""Handles backend of hyperclocked website."""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_marshmallow import Marshmallow
from flask_cors import CORS

__author__ = "Mitchell Clark"

# Initialise app.
app = Flask(__name__)
CORS(app)

app_settings = {
    "SQLALCHEMY_DATABASE_URI": "mysql://root@localhost/hyperclocked",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False
}
app.config.update(app_settings)

# Initialise database.
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Customers(db.Model):
    """Relation containing customer information. Contains a user id, first name, last name, email, hash and salt.
    The primary key is the id."""
    __tablename__ = "Customers"

    # Integer primary key automatically auto increments
    _id = db.Column(db.Integer, primary_key=True)
    _first_name = db.Column(db.String(100))
    _last_name = db.Column(db.String(100))
    _email = db.Column(db.String(100))
    _hash = db.Column(db.String(100))
    _salt = db.Column(db.String(100))

    _orders = relationship("Orders")

    def __init__(self, first_name, last_name, email, hash, salt):
        """Initialises new Customers instance."""
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._hash = hash
        self._salt = salt


class Orders(db.Model):
    """Relation containing order information. Contains customer id, order number and the total price of the order.
    Has the composite key of customer id and order num. Customer id references the id in the Customer relation."""
    __tablename__ = "Orders"

    _customer_id = db.Column(db.Integer, ForeignKey(
        "Customers._id"), primary_key=True)
    _order_num = db.Column(db.Integer, primary_key=True)
    _total_price = db.Column(db.Float)

    def __init__(self, customer_id, order_num, total_price):
        """Initialises new Orders instance."""
        self._customer_id = customer_id
        self._order_num = order_num
        self._total_price = total_price


# class ProductsInOrder(db.Model):
    """Relation containing products and their quantities in orders. Contains customer id, order number, product id, quantity 
    and total price. The composite key is customer id, order number and product id. Customer id  and order number 
    references customer id and order number in orders. Product id references id in Products."""
    # _customer_id = db.Column(db.)


class CustomersSchema(ma.Schema):
    """Marshmallow schema for serialising data of customers relation."""
    class meta:
        fields = ("_id", "_first_name", "_last_name",
                  "_email", "_hash", "_salt")


customer_schema = CustomersSchema()
customers_schema = CustomersSchema(many=True)


@ app.route('/', methods=["GET"])
def load_home():
    """Load the home page of hyperclocked."""
    return jsonify({"Hello": "World"})


@ app.route("/add", methods=["POST"])
def add_customer():
    """Add a customer."""
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    email = request.json["email"]
    hash = request.json["hash"]
    salt = request.json["salt"]

    customers = Customers(first_name, last_name, email, hash, salt)
    db.session.add(customers)
    db.session.commit
    return customer_schema.jsonify(customers)


@ app.route("/get/", methods=["GET"])
def get_all():
    all_customers = Customers.query.all()
    results = customers_schema.dump(all_customers)
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
