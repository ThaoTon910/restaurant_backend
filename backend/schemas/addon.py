
from datetime import datetime
from marshmallow import fields
from schemas import BaseSchema
from typing import Union, Optional

class AddonSchema(BaseSchema):
    #Resource
    addonGroupId = fields.UUID(required=True, attribute="addon_group_id")
    name = fields.String(required=True)
    price = fields.Float(required=True, type=Optional[float], allow_none=True)
    description = fields.String(required=True, type=Optional[str], allow_none=True)
    isTaxable = fields.Boolean(required=False, missing=True, attribute="is_taxable")

    # Dump to UI
    id = fields.String(dump_only=True)
    createdTime = fields.DateTime(dump_only=True, format='iso8601', attribute="created_time")
    updatedTime = fields.DateTime(dump_only=True, format='iso8601', attribute="updated_time")



if __name__ == '__main__':
    addon_schema = AddonSchema()
    addon_json = {
        'name':'ko hanh',
        'price': None,
        'description': None,
        'isTaxable': False,
        'addonGroupId': '2a85cd19-c7e2-4bf5-8c75-df167e3a4bd5'
    }
    # loaded = addon_schema.load(addon_json)
    # print(loaded)
    print(addon_schema.load(addon_json))
    print(addon_json)
