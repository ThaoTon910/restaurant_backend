from marshmallow import fields
from schemas import BaseSchema
from typing import Union
# dump: creates json
#load: creates dto object
class MenuItemSchema(BaseSchema):
    #Resource
    categoryId = fields.UUID(required=True, attribute="category_id")
    name = fields.String(required=True)
    description = fields.String(required=True, allow_none=True)
    price = fields.Float(required=True)
    imageUrl = fields.String(required=True, attribute="image_url")
    active = fields.Boolean(required=True)
    isTaxable = fields.Boolean(required=False, missing=True, attribute="is_taxable")
    size = fields.String(required=True)
    taxRate = fields.Float(required=False, missing=None, attribute="tax_rate", type=Union[float, None], allow_none=True)

    #Dump to UI
    id = fields.UUID(dump_only=True)
    createdTime = fields.DateTime(dump_only=True,  attribute="created_time")
    updatedTime = fields.DateTime(dump_only=True, attribute="updated_time")

    #Extra
    addonGroupIds = fields.List(fields.UUID, dump_only=True, attribute="addon_group_ids")

if __name__ == "__main__":
    schema = MenuItemSchema()
    data = {
      "name": "French Fries",
      "description": "Khoai tay chien.",
      "price": 3.75,
      "size": "Regular",
      "imageUrl": "",
      "active": True,
      "isTaxable": True,
      "taxRate": None,
      "categoryId": "b4ab8d17-b3e3-4bbd-a418-94ac369867d3"
    }

    print(schema.load(data))