from attr import attrib, attrs, validators, Factory
from uuid import UUID, uuid4
from datetime import datetime
from dto_models.menu_item import MenuItemDTO
from typing import Optional, Dict, List
from schemas import BaseSchema
@attrs
class CategoryDTO(object):
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
    #extra
    menu_items =attrib(
        init=False,
        type=List[MenuItemDTO],
        default=[],
        # validator=validators.instance_of(List[MenuItemDTO])
    )

if __name__ == '__main__':
    import uuid
    from schemas.category import CategorySchema
    category_schema = CategorySchema()
    category_json = {
        'name': 'Appertizer',
        'index' : 0,
        #'id': uuid.uuid4(),
        #'abc': 'xyz'
    }

    loaded = category_schema.load(category_json)
    # loaded = {'name': Appertizer, 'index': 0}
    # -> **loaded (key : value) = 'name': Appertizer, 'index': 0
    # dto = CategoryDTO(name=loaded['name'],
    #                     index=loaded['index'],

    dto = CategoryDTO(**loaded)

    print(loaded)
    print(dto)
    output_json = category_schema.dumps(dto)
    print(output_json)

