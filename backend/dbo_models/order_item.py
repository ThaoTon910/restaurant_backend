from database import db
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

    id = db.Column(GUID, primary_key=True)
    created_time = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow,)

    def __init__(self,
                 id: Union[UUID, GUID],
                 name: str,
                 category_id: int,
                 description: str,
                 price: float,
                 size: str,
                 image_url: str,
                 active: bool,
                 is_taxable: bool,
                 tax_rate: float):
        self.id = id
        self.name = name
        self.category_id = category_id
        self.description = description
        self.price = price
        self.size = size
        self.image_url = image_url
        self.active = active
        self.is_taxable = is_taxable
        self.tax_rate = tax_rate