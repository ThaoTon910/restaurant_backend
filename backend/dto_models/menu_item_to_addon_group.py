from attr import attrib, attrs, validators, Factory
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, Dict
from schemas import BaseSchema
@attrs
class MenuItemToAddonGroupDTO(object):
    menu_item_id = attrib(
        init=True,
        type=UUID,
        validator=validators.instance_of(UUID),
    )

    addon_group_id = attrib(
        init=True,
        type=UUID,
        validator=validators.instance_of(UUID),
    )

