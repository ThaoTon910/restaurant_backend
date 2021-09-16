# dto_model/order_item.py
from attr import attrib, attrs, validators, Factory
from uuid import UUID, uuid4
from dto_models import customer
from datetime import datetime
from typing import Optional, Dict, List
from schemas import BaseSchema

@attrs
class OrderItemDTO(object):
    special_instruction = attrib(
        init=True,
        type=str,
        validator=validators.instance_of(str),
    )
    quantity = attrib(
        init=True,
        type=int,
        validator=validators.instance_of(int)
    )
    menu_item_id = attrib(
        init=True,
        type=UUID,
        validator=validators.instance_of(UUID),
    )
    add_ons = attrib(
        init=True,
        type=List[UUID]
    )