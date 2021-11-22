# schemas/customer.py
from marshmallow import fields
from schemas import BaseSchema


class CustomerSchema(BaseSchema):
    # Resource
    firstName = fields.String(required=True, attribute="first_name")
    lastName = fields.String(required=True, attribute="last_name")
    phone = fields.String(required=True, attribute="phone_number")
    email = fields.String(required=True)

    street = fields.String(required=False)
    city = fields.String(required=False)
    state = fields.String(required=False)
    zipcode = fields.Integer(required=False)
    rewardPoint = fields.Integer(required=False)
    id = fields.UUID(required=False)

    # Dump to UI
    createdTime = fields.DateTime(dump_only=True, format='iso8601')



