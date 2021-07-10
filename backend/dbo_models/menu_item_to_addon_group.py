from database import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import VARCHAR, Integer, DateTime, Boolean, Float, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from ._helper import GUID

class MenuItemToAddonGroupDBO(db.Model):
    __tablename__ = "menu-item-to-addon-group"

    menu_item = relationship("MenuItemDBO", backref="menu-item-to-addon-group")
    menu_item_id = db.Column(GUID, ForeignKey("menu-item.id"), primary_key=True, index=True, nullable=False)

    addon_group = relationship("AddonGroupDBO", backref="addon-group-to-menu-item")
    addon_group_id = db.Column(GUID, ForeignKey("addon-group.id"), primary_key=True, index=True, nullable=False)


    def __init__(self,
                 menu_item_id: Union[UUID, GUID],
                 addon_group_id: Union[UUID, GUID]):
        self.menu_item_id = menu_item_id
        self.addon_group_id = addon_group_id

