from database import db
from dbo_models.menu_item_to_addon_group import MenuItemToAddonGroupDBO
from dbo_models.addon_group import AddonGroupDBO
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import VARCHAR, Integer, DateTime, Boolean, Float, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from ._helper import GUID
class MenuItemDBO(db.Model):
    __tablename__ = "menuitem"
    category = relationship("CategoryDBO", backref="menu_items")

    category_id = db.Column(GUID, ForeignKey("category.id"), index=True, nullable=False)
    name = db.Column(VARCHAR(100), nullable=False)
    description = db.Column(VARCHAR(100), nullable=True)
    price = db.Column(Float, nullable=False)
    image_url = db.Column(String)
    active = db.Column(Boolean, nullable=False)
    is_taxable = db.Column(Boolean, nullable=False)
    size = db.Column(VARCHAR(100), nullable=False)
    tax_rate = db.Column(Float, nullable=True)

    addon_groups = relationship('AddonGroupDBO', secondary='menuitemtoaddongroup', lazy='subquery',
                                       back_populates="menu_items")

    id = db.Column(GUID, primary_key=True)
    created_time = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow,)
    updated_time = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args = UniqueConstraint('category_id', 'name', name='_category_name_uc')

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