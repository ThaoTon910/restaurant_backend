# schemas/extra_percentage_all.py
from marshmallow import fields
from schemas import BaseSchema

class ExtraPercentageAllSchema(BaseSchema):
    # Resource
    promotiontype_id = fields.UUID(required=True, attribute="promotiontype_id")
    percent_off = fields.Float(required=True)

    # Dump to UI
    id = fields.UUID(dump_only=True)
    updated_time = fields.DateTime(dump_only=True, format='iso8601')
