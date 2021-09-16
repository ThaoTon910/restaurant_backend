from attr import attrib, attrs, validators, Factory
from uuid import UUID, uuid4
from datetime import datetime


@attrs
class PromotionTypeDTO(object):
    promotion_type = attrib(
        init=True,
        type=str,
        validator=validators.instance_of(str)
    )
    description = attrib(
        init=True,
        type=str,
        validator=validators.instance_of(str)
    )
    created_time = attrib(
        init=False,
        type=datetime,
        default=Factory(datetime.utcnow),
        validator=validators.instance_of(datetime)
    )
    id = attrib(
        type=UUID,
        default=Factory(uuid4),
        validator=validators.instance_of(UUID)
    )
