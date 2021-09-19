""" Test cases for API endpoints """
import json
from app.models import CustomerModel


def test_create_customer(app, session):
    """Test POST on '/customer' endpoint with correct JSON body"""
    data = {
        "first_name": "Jhon",
        "last_name": "Doe",
        "email": "j_doe@example.com",
        "zipcode": 20024,
    }
    client = app.test_client()
    response = client.post(
        "/customer", data=json.dumps(data), headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 201
    assert "user_id" in response.json
    # Checks user exists in db
    customer = CustomerModel.query.filter_by(email=data.get("email")).first()
    assert customer._id == response.json["user_id"]
