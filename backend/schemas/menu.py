from datetime import datetime
from marshmallow import fields
from schemas import BaseSchema
from schemas.category import CategorySchema
from schemas.menu_item import MenuItemSchema
from schemas.addon import AddonSchema
from schemas.addon_group import AddonGroupSchema
# dump: creates json, send back to UI
#load: creates dto object

class MenuSchema(BaseSchema):
    #Resource
    categories = fields.List(CategoryMenuSchema)
