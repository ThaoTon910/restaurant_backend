from database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import VARCHAR, Integer, DateTime, Boolean, Float, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from ._helper import GUID
from dbo_models.order_dbo import OrderDBO
from dbo_models.menu_item import MenuItemDBO
from dbo_models.menu_item_to_addon_group import MenuItemToAddonGroupDBO
from dbo_models.addon_group import AddonGroupDBO


class OrderItemDBO(db.Model):
    __tablename__ = "orderitem"
    order = relationship("OrderDBO", backref="order_items")
    order_id = db.Column(GUID, ForeignKey("order.id"), index=True, nullable=False)
    price = db.Column(Float, nullable=False)
    quantity = db.Column(Integer, nullable=False)
    special_instruction = db.Column(VARCHAR(100), nullable=True)
    menu_item = relationship("MenuItemDBO")
    menu_item_id = db.Column(GUID, ForeignKey("menuitem.id"), index=True, nullable=False)

    add_ons = relationship('AddonDBO', secondary='addontoorderitem', lazy='subquery',
                           back_populates="order_item")

    id = db.Column(GUID, primary_key=True, default=uuid.uuid4 )
    created_time = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, )

    def __init__(self, order: OrderDBO, menu_item: MenuItemDBO, quantity: Integer = 0, special_instruction=""):
        self.order_id = order.id
        self.order = order
        self.menu_item_id = menu_item.id
        self.menu_item = menu_item
        self.price = 0
        self.quantity = quantity
        self.special_instruction=special_instruction
