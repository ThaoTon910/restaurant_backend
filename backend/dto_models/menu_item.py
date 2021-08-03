from attr import attrib, attrs, validators, Factory
from datetime import datetime
from uuid import UUID, uuid4
from typing import Union, List

@attrs
class MenuItemDTO(object):
    category_id = attrib(
        init=True,
        type=UUID,
        validator=validators.instance_of(UUID),
    )
    name = attrib(
        init=True,
        type=str,
        validator=validators.instance_of(str)
    )

    description = attrib(
        init=True,
        type=str,
        validator=validators.optional(validators.instance_of(str)),
    )
    price = attrib(
        init=True,
        type=float,
        validator=validators.instance_of(float),
    )
    image_url = attrib(
        init=True,
        type=str,
        validator=validators.instance_of(str),
    )
    active = attrib(
        init=True,
        type=bool,
        validator=validators.instance_of(bool),
    )
    is_taxable = attrib(
        init=True,
        type=bool,
        validator=validators.instance_of(bool),
    )
    size = attrib(
        init=True,
        type=str,
        validator=validators.instance_of(str),
    )

    tax_rate = attrib(
        init=True,
        type=Union[float, None],
        default=None,
        validator=validators.optional(validators.instance_of(float)),
    )
    id = attrib(
        init=True,
        type=UUID,
        default=Factory(uuid4),
        validator=validators.instance_of(UUID),
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
    #Extra
    addon_group_ids = attrib(
        init=False,
        type=List[UUID],
        default=[],
        validator=validators.instance_of(list)
    )
