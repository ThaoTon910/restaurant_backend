# schemas/order_schema.py
from marshmallow import fields
from schemas import BaseSchema
from schemas.order_schema import OrderSchema

class OrderResponseSchema(BaseSchema):
    order = fields.Nested(OrderSchema)
    clientSecret = fields.String(required=True, dump_only=True)