""" This module holds all the gis tasks """

from flask import Blueprint
import click
import requests
import mpu
import os

from app.models import CustomerModel, LocationRank, db
from app.util.dictionary import DictUtils
from app.util.redis import RedisHelper


gis = Blueprint("gis", __name__)


class GIS:
    """Class definition to handle GIS operations"""

    CUSTOMER_MODEL = CustomerModel
    LOCATION_MODEL = LocationRank
    REDIS_URI = os.getenv("REDIS_URI")
    ZIP_API_URL = os.getenv("ZIP_API_URL")
    REDIS_HELPER = RedisHelper(REDIS_URI)
    KM_TO_MILES_FACTOR = 0.6213712

    @classmethod
    def get_lat_lon_data(cls, zipcode):
        response = requests.get(cls.ZIP_API_URL.format(zipcode))
        if response.status_code == 200:
            lat_lon = DictUtils.search_multiple_keys(response.json(), ["lat", "lng"])
            lat, lon = lat_lon[0], lat_lon[1]
            return {"lat": lat, "lon": lon}

    @classmethod
    def get_zipcode_data(cls, zipcode):
        return cls.REDIS_HELPER.get_value(zipcode)

    @classmethod
    def insert_zipcode_data(cls, zipcode, zipcode_data):
        cls.REDIS_HELPER.set_value(zipcode, zipcode_data)

    @classmethod
    def calc_distance_btw_zipcodes(cls, zipcodes: list, units="km"):
        """Returns the distance in kms between 2 zipcodes"""
        for zipcode in zipcodes:
            # Get latitude and longitude from external API
            lat_lon_data = cls.get_lat_lon_data(zipcode)
            # Update zipcodes data source
            cls.insert_zipcode_data(zipcode, lat_lon_data)
        zipcodes_info = cls.REDIS_HELPER.get_multiple_values(zipcodes)
        zipcode1 = (zipcodes_info[0]["lat"], zipcodes_info[0]["lon"])
        zipcode2 = (zipcodes_info[1]["lat"], zipcodes_info[1]["lon"])
        distance = round(mpu.haversine_distance(zipcode1, zipcode2), 3)
        if units == "km":
            print(distance)
            return distance
        elif units == "miles":
            return round(distance * cls.KM_TO_MILES_FACTOR, 3)


@gis.cli.command("calc_distance")
@click.argument("zipcode1")
@click.argument("zipcode2")
@click.option("--units")
def calc_distance(zipcode1, zipcode2, units):
    if not units:
        units = "km"
    distance = GIS.calc_distance_btw_zipcodes([zipcode1, zipcode2], units)
    print(f"Distance is: {distance} {units}")
