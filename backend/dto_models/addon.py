
from attr import attrib, attrs, validators, Factory
from uuid import UUID, uuid4
from datetime import datetime
from typing import Union
from schemas import BaseSchema
@attrs
class AddonDTO():
    addon_group_id = attrib(
        init=True,
        type=UUID,
        validator=validators.instance_of(UUID),
    )
    name = attrib(
        init=True,
        type=str,
        validator=validators.instance_of(str)
    )
    price = attrib(
        init=True,
        type=float,
        validator=validators.optional(validators.instance_of(float)),
    )

    description = attrib(
        init=True,
        type=str,
        validator=validators.optional(validators.instance_of(str)),
    )

    is_taxable = attrib(
        init=True,
        type=bool,
        validator=validators.instance_of(bool),
    )

    id = attrib(
        type=UUID,
        default=Factory(uuid4),
        validator=validators.instance_of(UUID),
    )

    created_time = attrib(
        init=False,
        type=datetime,
        default=Factory(datetime.utcnow),
        validator=validators.instance_of(datetime)
    )
    updated_time = attrib(
        init=False,
        type=datetime,
        default=Factory(datetime.utcnow),
        validator=validators.instance_of(datetime),
    )

if __name__ == "__main__":
    from schemas.addon import AddonSchema
    import uuid
    schema = AddonSchema()
    #Note: input of UI is camel case (not snake case)
    addon_json ={
        'id': 1,
        'addonGroupId': "2a85cd19-c7e2-4bf5-8c75-df167e3a4bd5",
        'name': 'Khong hanh',
        'price': None,
        'description': None,
        'is_taxable': None
    }
    #validated json (schema)
    loaded = schema.load(addon_json)
    #DTO
    dto = AddonDTO(**loaded)

    print("json dictionary:")
    print(loaded)

    print("data transform:")
    print(dto)


