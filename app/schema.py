""" Schemas definitions """
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import auto_field

from .models import CustomerModel

ma = Marshmallow()


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CustomerModel
        exclude = ["_id"]

    user_id = auto_field("_id", dump_only=True)
