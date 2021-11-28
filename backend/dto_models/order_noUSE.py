# dto_model/order.py
from attr import attrib, attrs, validators, Factory
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, Dict, List
from schemas import BaseSchema
from dto_models.customer import CustomerDTO
from dto_models.order_item import OrderItemDTO


@attrs
class OrderDTO(object):
    payment_token = attrib(
        init=True,
        type=str,
        validator=validators.instance_of(str),
    )
    promo_code = attrib(
        init=True,
        type=str,
        validator=validators.instance_of(str),
    )
    customer = attrib(
        init=True,
        type=CustomerDTO,
    )
    items = attrib(
        init=True,
        type=List[OrderItemDTO]
    )
    tax_multiplier = attrib(
        init=True,
        type=float
    )
    tip_multiplier = attrib(
        init=True,
        type=float
    )


