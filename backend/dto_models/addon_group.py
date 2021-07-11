from attr import attrib, attrs, validators, Factory
from uuid import UUID, uuid4
from datetime import datetime
from dto_models.addon import AddonDTO
from typing import List

@attrs
class AddonGroupDTO(object):
    name = attrib (
        init=True,
        type=str,
        validator=validators.instance_of(str)
    )
    max_quantity = attrib(
        init=True,
        type=int,
        validator=validators.optional(validators.instance_of(int)),
    )
    min_quantity = attrib (
        init=True,
        type=int,
        validator=validators.optional(validators.instance_of(int))
    )
    id = attrib(
        init=False,
        type=UUID,
        default=Factory(uuid4),
        validator=validators.instance_of(UUID)
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
    # extra
    addons = attrib(
        init=False,
        type=List[AddonDTO],
        default=[],
        # validator=validators.instance_of(List[MenuItemDTO])
    )

if __name__== '__main__':
    from schemas.addon_group import AddonGroupSchema

    addon_group_json = {
        'name': 'Group 1',
        'maxQuantity': 3,
        'minQuantity': 0,
    }
    addon_group_schema = AddonGroupSchema()
    loaded = addon_group_schema.load(addon_group_json)
    # loaded = {'max_quantity': 3, 'min_quantity': 0, 'name': 'Group 1'}
    # -> **loaded (key : value) = 'max_quantity': 3, 'min_quantity': 0, 'name': 'Group 1'
    # dto = AddonGroupDTO(name=loaded['name'],
    #                     max_quantity=loaded['max_quantity'],
    #                     min_quantity=loaded['min_quantity'])

    dto = AddonGroupDTO(**loaded)
    print("loaded = {}".format(loaded))
    print(dto)
