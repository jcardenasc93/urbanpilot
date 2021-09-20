""" Models definition """

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

import re

# Instace db
db = SQLAlchemy()


class CustomerModel(db.Model):
    __tablename__ = "customer"
    email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    _id = db.Column("id", db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    middle_name = db.Column(db.String(20), nullable=True)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(20), nullable=True)
    county = db.Column(db.String(20), nullable=True)
    state = db.Column(db.String(20), nullable=True)

    @validates("email")
    def email_validation(self, key, value):
        self.not_empty_value(key, value)
        if re.fullmatch(self.email_regex, value):
            return value
        raise ValueError("Invalid email")

    @validates("zipcode")
    def zipcode_validation(self, key, value):
        if value > 0 and len(str(value)) == 5:
            return value
        raise ValueError("Invalid zipcode")

    @validates("first_name")
    def firs_name_validation(self, key, value):
        self.not_empty_value(key, value)
        return value

    @validates("last_name")
    def last_name_validation(self, key, value):
        self.not_empty_value(key, value)
        return value

    def __init__(self, first_name, last_name, email, zipcode, middle_name=None):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.zipcode = zipcode

    @staticmethod
    def not_empty_value(key, value):
        if value == "":
            raise ValueError(f"Not allowed empty values for {key}")

    def __repr__(self):
        # Overrides object representation
        return f"{self.email}: {self.zipcode}"


class LocationRank(db.Model):
    __tablename__ = "location_rank"

    zipcode = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(20), nullable=False)
    frecuency = db.Column(db.Integer, nullable=False)

    @validates("zipcode")
    def zipcode_validation(self, key, value):
        if value > 0 and len(str(value)) == 5:
            return value
        raise ValueError("Invalid zipcode")

    def __init__(self, zipcode, city, frecuency):
        self.zipcode = zipcode
        self.city = city
        self.frecuency = frecuency

    def __repr__(self):
        return f"| {self.zipcode} | {self.city} | {self.frecuency} |"
