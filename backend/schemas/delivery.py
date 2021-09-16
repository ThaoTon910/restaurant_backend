# schemas/delivery.py
from marshmallow import fields
from schemas import BaseSchema


class DeliverySchema(BaseSchema):
    # Resource
    deliveryType = fields.String(required=True)
    deliveryFee = fields.Float(required=True)



