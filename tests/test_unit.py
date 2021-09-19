""" Test cases for specific application components """

import pytest
from unittest.mock import patch
from app.tasks.location import ZipCodeLocation, search_for_location
from app.models import CustomerModel


async def test_search_location_info(session, celery_app, celery_worker):
    external_call_mock_value = {
        "zip_code": "33411",
        "lat": 0.46635,
        "lng": -1.39963,
        "city": "West Palm Beach",
        "state": "FL",
    }
    with patch.object(
        ZipCodeLocation, "get_location_info", return_value=external_call_mock_value
    ):
        test_customer = CustomerModel(
            first_name="Jhon", last_name="Doe", email="j_doe@example.co", zipcode=33411
        )
        session.add(test_customer)
        session.commit()
        assert test_customer._id > 0
        search_for_location.delay(test_customer._id, 33411).get()
        assert test_customer.city == external_call_mock_value["city"]
