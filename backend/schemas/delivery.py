# schemas/delivery.py
from marshmallow import fields
from schemas import BaseSchema

class PickUPSchema(BaseSchema):
    deliveryType = fields.String(required=True, attribute="delivery_type")
    merchantId = fields.UUID(required=True, attribute="merchant_id")
    time =  fields.DateTime( format='iso8601')

class DeliverySchema(BaseSchema):
    # Resource
    deliveryFee = fields.Float(required=True, attribute="delivery_fee")
    info = fields.Nested(PickUPSchema)



