# schemas/promotion.py
from marshmallow import fields
from schemas import BaseSchema


class PromotionSchema(BaseSchema):
    # Resource
    promotiontype_id = fields.UUID(required=True, attribute="promotiontype_id")
    description = fields.String(required=True,  attribute="description")
    is_active = fields.Boolean(required=True,  attribute="is_active")
    start_date = fields.DateTime(required=True,  attribute="start_date")
    end_date = fields.DateTime(required=True,  attribute="end_date")
    image_url = fields.String(required=True,  attribute="image_url")
    promo_code = fields.String(required=True, allow_none=True,  attribute="promo_code")


    # Dump to UI
    id = fields.UUID(dump_only=True)
    createdTime = fields.DateTime(dump_only=True, attribute="created_time")

