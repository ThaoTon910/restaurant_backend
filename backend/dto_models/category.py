from attr import attrib, attrs, validators, Factory
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, Dict

@attrs
class Category(object):
    name = attrib(
        init=True,
        type=str,
        validator=validators.instance_of(str),
    )
    index = attrib(
        init=True,
        type=int,
        validator=validators.instance_of(int),
    )

    created_time = attrib(
        init=False,
        type=datetime,
        default=Factory(datetime.utcnow),
        validator=validators.instance_of(datetime),
    )

    updated_time = attrib(
        init=False,
        type=datetime,
        default=Factory(datetime.utcnow),
        validator=validators.instance_of(datetime),
    )

    id = attrib(
        type=UUID,
        default=Factory(uuid4),
        validator=validators.instance_of(UUID),
    )

if __name__ == '__main__':
    import uuid
    from schemas.category import CategorySchema
    category_schema = CategorySchema()
    category_json = {
        'name': 'Appertizer',
        'index' : 0,
        'id': uuid.uuid4(),
        'abc': 'xyz'
    }

    category_dto = category_schema.load(category_json)
    dto = Category(**category_dto)

    print(category_dto)
    print(dto)


    output_json = category_schema.dumps(dto)
    print(output_json)

