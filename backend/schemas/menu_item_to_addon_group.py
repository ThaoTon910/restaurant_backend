from datetime import datetime
from marshmallow import fields
from schemas import BaseSchema
# dump: creates json, send back to UI
#load: creates dto object

class MenuItemToAddonGroupSchema(BaseSchema):
    #Resource
    menuItemId = fields.UUID(required=True, attribute="menu_item_id")
    addonGroupId= fields.UUID(required=True, attribute="addon_group_id")

if __name__ == '__main__':
    schema = MenuItemToAddonGroupSchema()
    data_json = {
        'menuItemId': "3d791d3f-b0d6-4637-9cbd-65f448ad2cd8",
        'addonGroupId': "23cae19a-4f0c-4305-89b2-abc0c4e344df"
    }
    print(schema.load(data_json))