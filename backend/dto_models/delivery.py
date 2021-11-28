# dto_models/delivery.py
from attr import attrib, attrs, validators, Factory


@attrs
class DeliveryDTO(object):
    delivery_type = attrib(
        init=True,
        type=str,
        validator=validators.instance_of(str)
    )
    delivery_fee = attrib(
        init=True,
        type=float,
        validator=validators.instance_of(float)
    )
