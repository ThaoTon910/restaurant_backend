# dto_models/promotion.py
from attr import attrib, attrs, validators, Factory
from uuid import UUID, uuid4
from datetime import datetime


@attrs
class PromotionDTO:
    promotiontype_id = attrib(
        init=True,
        type=UUID,
        validator=validators.instance_of(UUID),
    )
    description = attrib(
        init=True,
        type=str,
        validator=validators.instance_of(str)
    )
    is_active = attrib(
        init=True,
        type=bool,
        validator=validators.instance_of(bool),
    )
    start_date = attrib(
        init=True,
        type=datetime,
        validator=validators.instance_of(datetime)
    )
    end_date = attrib(
        init=True,
        type=datetime,
        validator=validators.instance_of(datetime)
    )
    created_time = attrib(
        init=False,
        type=datetime,
        default=Factory(datetime.utcnow),
        validator=validators.instance_of(datetime)
    )
    image_url = attrib(
        init=True,
        type=str,
        validator=validators.instance_of(str)
    )
    promo_code = attrib(
        init=True,
        type=str,
        validator=validators.instance_of(str)
    )
    id = attrib(
        type=UUID,
        default=Factory(uuid4),
        validator=validators.instance_of(UUID),
    )
