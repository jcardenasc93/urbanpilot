""" Models definition """

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

# Instace db
db = SQLAlchemy()


class CustomerModel(db.Model):
    __tablename__ = "customer"

    _id = db.Column("id", db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    middle_name = db.Column(db.String(20), nullable=True)
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True)
    zipcode = db.Column(db.Integer)

    @validates("email")
    def email_validation(self, key, value):
        assert "@" in value
        return value

    @validates("zipcode")
    def zipcode_validation(self, key, value):
        assert value > 0
        assert len(str(value)) == 5
        return value

    def __init__(self, first_name, last_name, email, zipcode, middle_name=None):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.email = email
        self.zipcode = zipcode

    def __repr__(self):
        # Overrides object representation
        return f"{self.email}: {self.zipcode}"
