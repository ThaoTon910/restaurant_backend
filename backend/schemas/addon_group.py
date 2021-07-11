from marshmallow import fields
from schemas import BaseSchema
from typing import Union
from schemas.addon import AddonSchema
from datetime import datetime
class  AddonGroupSchema(BaseSchema):
    #Resource
    name = fields.String(required=True)
    maxQuantity = fields.Integer(required=True, type=Union[int, None], attribute="max_quantity", allow_none=True)
    minQuantity = fields.Integer(required=True, type=Union[int, None], attribute="min_quantity", allow_none=True)

    # Dump to UI
    id = fields.UUID(dump_only=True)
    createdTime = fields.DateTime(dump_only=True, format='iso8601', attribute="created_time")
    updatedTime = fields.DateTime(dump_only=True, format='iso8601', attribute="updated_time")
    # extra
    addons = fields.List(fields.Nested(AddonSchema), dump_only=True)

# Test
if __name__ == '__main__':
    addon_group_schema = AddonGroupSchema()
    addon_group_json = {
        'name':'Group 1',
        'maxQuantity': 3,
        'minQuantity': 0,
    }

    loaded = addon_group_schema.load(addon_group_json)
    print(loaded)
    #print(addon_group_schema.load(addon_group_json))


