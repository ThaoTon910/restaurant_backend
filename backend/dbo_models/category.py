from database import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import VARCHAR, Integer, DateTime
from datetime import datetime
from typing import Union
from ._helper import GUID

class CategoryDBO(db.Model):
    __tablename__ = "category"
    name = db.Column(VARCHAR(100), nullable=False)
    index = db.Column(Integer)

    id = db.Column(GUID, primary_key=True)
    created_time = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_time = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, id: Union[UUID, GUID],
                 name: str,
                 index: int):
        self.id = id
        self.name = name
        self.index = index
