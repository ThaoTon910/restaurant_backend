from database import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import VARCHAR, Integer, DateTime, Boolean, Float, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from ._helper import GUID

class AddonToOrderItem(db.Model):
    __tablename__ = "addontoorderitem"

    order_item_id = db.Column(GUID, ForeignKey("orderitem.id", ondelete='CASCADE'), primary_key=True, index=True,
                              nullable=False)
    addon_id = db.Column(GUID, ForeignKey("addon.id", ondelete='CASCADE'), primary_key=True, index=True, nullable=False)


    def __init__(self,
                 order_item_id: Union[UUID, GUID],
                 addon_id: Union[UUID, GUID]):
        self.order_item_id = order_item_id
        self.addon_id = addon_id

