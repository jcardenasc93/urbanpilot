""" Realte zipcodes with real locations """
import os
import requests
import time
from celery import shared_task


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
        time.sleep(5)
        return response


@shared_task(name="celery_tasks.search_for_location")
def search_for_location(zipcode: int):
    zipcode_to_location = ZipCodeLocation(zipcode)
    response = zipcode_to_location.get_location_info()
    print(response)
