# dto_models/extra_percentage_all.py
from attr import attrib, attrs, validators, Factory
from uuid import UUID, uuid4
from datetime import datetime


@attrs
class ExtraPercentageAllDTO(object):
    promotiontype_id = attrib(
        init=True,
        type=UUID,
        validator=validators.instance_of(UUID),
    )
    percent_off = attrib(
        init=True,
        type=float,
        validator=validators.instance_of(float)
    )
    updated_time = attrib(
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
