from database import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import VARCHAR, Integer, DateTime
from datetime import datetime
from typing import Union
from ._helper import GUID

class AddonGroupDBO(db.Model):
    __tablename__ = "addon-group"
    name = db.Column(VARCHAR(100), nullable=False)
    max_quantity = db.Column(Integer)
    min_quantity = db.Column(Integer)

    id = db.Column(GUID, primary_key=True)
    created_time = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow())
    updated_time = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def __init__(self, id: Union[UUID, GUID],
                 name: str,
                 max_quantity:int,
                 min_quantity: int):
        self.id = id
        self.name = name
        self.max_quantity = max_quantity
        self.min_quantity = min_quantity
