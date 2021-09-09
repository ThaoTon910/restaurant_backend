# schemas/customer.py
from marshmallow import fields
from schemas import BaseSchema


class CustomerSchema(BaseSchema):
    # Resource
    firstName = fields.String(required=True)
    surname = fields.String(required=True)
    phone = fields.String(required=True)
    email = fields.String(required=True)
    street = fields.String(required=False)
    city = fields.String(required=False)
    state = fields.String(required=False)
    zipcode = fields.Integer(required=False)
    rewardPoint = fields.Integer(required=False)

    # Dump to UI
    id = fields.UUID(dump_only=True)
    createdTime = fields.DateTime(dump_only=True, format='iso8601')



