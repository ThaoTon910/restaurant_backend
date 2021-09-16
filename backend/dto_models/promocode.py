# dto_models/promocode.py
from attr import attrib, attrs, validators

@attrs
class PromoCodeDTO:
    promo_code = attrib(
        init=True,
        type=str,
        validator=validators.instance_of(str)
    )
    order_item = attrib(
        init=True,
        type=dict
    )
    sub_total = attrib(
        init=True,
        type=float,
        validator=validators.instance_of(float)
    )
    total_discount = attrib(
        init=True,
        type=float,
        validator=validators.instance_of(float)
    )
    shipping_fee = attrib(
        init=True,
        type=float,
        validator=validators.instance_of(float)
    )
    shipping_discount = attrib(
        init=True,
        type=float,
        validator=validators.instance_of(float)
    )
