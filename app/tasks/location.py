""" Realte zipcodes with real locations """
import os
import requests
from celery import shared_task
from app.util.utils import DictUtils
from app.tasks.celery_setup import make_celery

celery = make_celery()
from app.models import db, CustomerModel

class ZipCodeLocation:
    """Class defined to retrieve locations based on a zipcode"""

    SOURCE_URL = os.getenv("ZIP_API_URL")

    def __init__(self, zipcode: int):
        self.__city = None
        self.__county = None
        self.__state = None
        self.zipcode = zipcode

    @property
    def city(self):
        return self.__city

    @property
    def county(self):
        return self.__county

    @property
    def state(self):
        return self.__state

    def validate_ok_response(func):
        """Decorator to check for HTTP 200 status code"""

        def wrapper(self):
            response = func(self)
            if response.status_code == 200:
                return response
            return None

        return wrapper

    @validate_ok_response
    def get_location_info(self):
        """Retrieves location info from external source based on the zipcode"""
        request_url = self.SOURCE_URL.format(self.zipcode)
        response = requests.get(request_url)
        return response


@shared_task(name="celery_tasks.search_for_location")
def search_for_location(customer_id: int, zipcode: int):
    zipcode_to_location = ZipCodeLocation(zipcode)
    response = zipcode_to_location.get_location_info()
    # If response status code is 200 then updates customer's info
    if response:
        response = response.json()
        city = DictUtils.search_key("city", response)
        state = DictUtils.search_key("state", response)
        county = DictUtils.search_key("county", response)
        try:
            # with celery.app.app_context():
            CustomerModel.query.filter_by(_id=customer_id).update(
                dict(city=city, state=state, county=county)
            )
            db.session.commit()
        except Exception as e:
            print(e)
