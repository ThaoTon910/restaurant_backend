# schemas/order_schema.py
from marshmallow import fields
from schemas import BaseSchema
from schemas.customer import CustomerSchema
from schemas.delivery import DeliverySchema
from schemas.order_item import OrderItemSchema

class OrderSchema(BaseSchema):

    customer = fields.Nested(CustomerSchema)
    delivery = fields.Nested(DeliverySchema)
    items = fields.List(fields.Nested(OrderItemSchema), required=True)
    paymentToken = fields.String(required=False, attribute="payment_token")
    promoCode = fields.String(required=False, attribute="promo_code")
    taxMultiplier = fields.Float(required=True, attribute="tax_multiplier")
    tipMultiplier = fields.Float(required=True, attribute="tip_multiplier")

    status = fields.String(required=True, dump_only=True)
    discount = fields.Float(required=True, dump_only=True)
    id = fields.UUID(dump_only=True)