# schemas/promocode.py
from marshmallow import fields
from schemas import BaseSchema

class PromoCodeSchema(BaseSchema):
    # promo code

    promo_code = fields.String(required=True) #  attribute="promo_code")

    # order detail
    order_item = fields.Dict(required=True)
    sub_total = fields.Float(required=True)
    total_discount = fields.Float(required=True)
    shipping_fee = fields.Float(required=True)
    shipping_discount = fields.Float()





