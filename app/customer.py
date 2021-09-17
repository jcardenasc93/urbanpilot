""" Views implementation """

from flask import Blueprint, request
from .models import db, CustomerModel
from .schema import CustomerSchema

# Instance blueprint
customer = Blueprint("customer", __name__)

# Schemas definition
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


@customer.route("", methods=["POST"])
def register_customer():
    first_name = request.json.get("first_name")
    middle_name = request.json.get("middle_name")
    last_name = request.json.get("last_name")
    email = request.json.get("email")
    zipcode = request.json.get("zipcode")

    try:
        new_customer = CustomerModel(first_name, last_name, email, zipcode, middle_name)
        db.session.add(new_customer)
        db.session.commit()
    except Exception as e:
        return {"server_msg": "Invalid request", "error_msg": e.__str__()}, 400
    else:
        return customer_schema.jsonify(new_customer), 201
