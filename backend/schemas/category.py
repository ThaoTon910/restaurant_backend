from datetime import datetime
from marshmallow import fields
from schemas import BaseSchema
from schemas.menu_item import MenuItemSchema
from typing import List
# dump: creates json, send back to UI
#load: creates dto object

class CategorySchema(BaseSchema):
    #Resource
    name = fields.String(required=True)
    index = fields.Integer(required=True)
    #Dump to UI
    id = fields.UUID(dump_only=True)
    createdTime = fields.DateTime(dump_only=True, format='iso8601', attribute="created_time")
    updatedTime = fields.DateTime(dump_only=True, format='iso8601', attribute="updated_time")
    #extra
    menuItems = fields.List(fields.Nested(MenuItemSchema), dump_only=True, attribute="menu_items")

# Test

if __name__ == '__main__':
    import uuid
    category_schema = CategorySchema()
    category_json = {
        'name': 'Appertizer',
        'index' : 0,
        'id': uuid.uuid4(),
        'abc': 'xyz',
        # 'createdTime': datetime.datetime.now()
    }

    class CategoryDTO():
        def __init__(self, name, index):
            self.name = name
            self.index = index

    print("load to dto")
    category_dto = category_schema.load(category_json)
    #dto = CategoryDTO(**category_dto)
    print(category_dto)


    print("dump to UI json")
    category_dto['created_time'] = datetime.datetime.now()

    loaded_json = category_schema.dumps(category_dto)
    print(loaded_json)

