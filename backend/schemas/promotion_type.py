from marshmallow import fields
from schemas import BaseSchema

# dump: creates json, send back to UI
#load: creates dto object

class PromotionTypeSchema(BaseSchema):
    # Resource
    promotion_type = fields.String(required=True)
    description = fields.String(required=True)

    # Dump to UI
    id = fields.UUID(dump_only=True)
    created_time = fields.DateTime(dump_only=True, format='iso8601')

