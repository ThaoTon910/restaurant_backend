from attr import attrib, attrs, validators, Factory
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, List
from dto_models.hour import HourDTO, check_hours
from dto_models._base import AsDict
@attrs
class MerchantDTO(AsDict):

    name = attrib(
        init=True,
        type=str,
        validator=validators.instance_of(str),
    )

    address = attrib(
        init=True,
        type=str,
        validator=validators.instance_of(str),
    )

    hours = attrib(
        type=List[HourDTO],
        validator=[validators.instance_of(List), check_hours],
    )

    id = attrib(
        type=UUID,
        default=Factory(uuid4),
        validator=validators.instance_of(UUID),
    )

    created_time = attrib(
        init=False,
        type=datetime,
        validator=validators.instance_of(datetime),
    )

    updated_time = attrib(
        init=False,
        type=datetime,
        validator=validators.instance_of(datetime),
    )

    phone = attrib(
        init=True,
        type=Optional[str],
        default="",
        validator=validators.optional(validators.instance_of(str)),
    )




