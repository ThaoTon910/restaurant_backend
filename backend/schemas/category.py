from marshmallow import fields, Schema
from schemas import BaseSchema
# dump: creates json
#load: creates dto object

class CategorySchema(BaseSchema):
    name = fields.String(required=True, type=str)
    index = fields.Integer(type=int)

    id = fields.UUID(dump_only=True)
    createdTime = fields.DateTime(required=False, dump_only=True, format='iso8601', attribute="created_time")
    updatedTime = fields.DateTime(required=False, dump_only=True, format='iso8601', attribute="updated_time")


# Test

if __name__ == '__main__':
    import uuid
    category_schema = CategorySchema()
    category_json = {
        'name': 'Appertizer',
        'index' : 0,
        'id': uuid.uuid4(),
        'abc': 'xyz'
    }

    class CategoryDTO():
        def __init__(self, name, index):
            self.name = name
            self.index = index

    category_dto = category_schema.load(category_json)
    #dto = CategoryDTO(**category_dto)
    print(category_dto)

