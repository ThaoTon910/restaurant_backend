from attr import attrib, attrs, validators, Factory
from uuid import UUID, uuid4
from datetime import datetime
from dto_models.menu_item import MenuItemDTO
from dto_models.addon_group import AddonGroupDTO
from dto_models.category import CategoryDTO
from typing import Optional, Dict, List
from schemas import BaseSchema
@attrs
class MenuDTO(object):

    #extra
    categories = attrib(
        init=True,
        type=List[CategoryDTO],
        # validator=validators.instance_of(List[MenuItemDTO])
    )
    addon_groups = attrib(
        init=True,
        type=List[AddonGroupDTO],
        # validator=validators.instance_of(List[MenuItemDTO])
    )




