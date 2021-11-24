"""Handles backend of hyperclocked website."""

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import PrimaryKeyConstraint

__author__ = "Mitchell Clark"

# Initialise app.
app = Flask(__name__)

app_settings = {
    "SQLALCHEMY_DATABASE_URI": "mysql://username:password@server/db",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False
}
app.config.update(app_settings)

# Initialise database.
db = SQLAlchemy(app)


class Customers(db.Model):
    """Relation containing customer information. Contains a user id, first name, last name, email, hash and salt.
    The primary key is the id."""
    _id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    _first_name = db.Column(db.String())
    _last_name = db.Column(db.String())
    _email = db.Column(db.String())
    _hash = db.Column(db.String())
    _salt = db.Column(db.String())

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
    _customer_id = db.Column(db.Integer, ForeignKey(
        "Customers.id"), primary_key=True)
    _order_num = db.Column(db.Integer, primary_key=True, auto_increment=True)
    _total_price = db.Column(db.Float)

    def __init__(self, customer_id, order_num, total_price):
        """Initialises new Orders instance."""
        self._customer_id = customer_id
        self._order_num = order_num
        self._total_price = total_price


class ProductsInOrder(db.Model):
    """Relation containing products and their quantities in orders. Contains customer id, order number, product id, quantity 
    and total price. The composite key is customer id, order number and product id. Customer id  and order number 
    references customer id and order number in orders. Product id references id in Products."""
    # _customer_id = db.Column(db.)


@ app.route('/', methods=["GET"])
def get_articles():
    return jsonify({"Hello": "World"})


if __name__ == "__main__":
    app.run(debug=True)
