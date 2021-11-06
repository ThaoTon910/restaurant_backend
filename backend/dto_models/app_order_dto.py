# dto_model/app_order_dto.py
from attr import attrib, attrs, validators, Factory
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional, Dict, List
from schemas import BaseSchema
from dto_models.customer import CustomerDTO
from dto_models.order_item import OrderItemDTO
from dto_models.delivery import DeliveryDTO
from dto_models.payment import PaymentDTO


@attrs
class OrderDTO(object):
    payment = attrib(
        init=False,
        type=PaymentDTO
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
    discount = attrib(
        init=False,
        type=float
    )
    delivery = attrib(
        init=True,
        type=DeliveryDTO
    )
    status = attrib(
        init=False,
        type=str
    )
    id = attrib(
        init=True,
        type=UUID,
        default=Factory(uuid4),
        validator=validators.instance_of(UUID),
    )


