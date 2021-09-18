""" Views implementation """

from flask import Blueprint, request, jsonify, current_app
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
        current_app.celery.send_task(
            "celery_tasks.search_for_location", args=[new_customer._id, zipcode]
        )

        return customer_schema.jsonify(new_customer), 201


@customer.route("", methods=["GET"])
def get_customers():
    customers = CustomerModel.query.all()
    response = customers_schema.dump(customers)
    return jsonify(response), 200


@customer.route("/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = CustomerModel.query.get(customer_id)
    return customer_schema.jsonify(customer), 200
