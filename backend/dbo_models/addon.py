from database import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import VARCHAR, Integer, DateTime, Boolean, Float, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from ._helper import GUID

class AddonDBO(db.Model):
    __tablename__ = "addon"
    addon_group = relationship("AddonGroupDBO", backref="addons")

    addon_group_id = db.Column(GUID, ForeignKey("addon-group.id"), index=True, nullable=False)
    id = db.Column(GUID, primary_key=True)
    name = db.Column(VARCHAR(100), nullable=False)
    price = db.Column(Float, nullable=True)
    description = db.Column(VARCHAR(100), nullable=True)
    is_taxable = db.Column(Boolean, nullable=False)
    created_time = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow())
    updated_time = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow(),
                             onupdate=datetime.utcnow())

    def __init__(self,
                 id: Union[UUID, GUID],
                 addon_group_id: Union[UUID, GUID],
                 name: str,
                 price: float,
                 description: str,
                 is_taxable: bool):
        self.id = id
        self.addon_group_id = addon_group_id
        self.name = name
        self.price = price
        self.description = description
        self.is_taxable = is_taxable

