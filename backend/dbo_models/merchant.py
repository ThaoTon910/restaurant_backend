from database import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import VARCHAR, String, JSON, DateTime
from datetime import datetime
from typing import Optional, Dict, Union
from ._helper import GUID


class MerchantDBO(db.Model):
    __tablename__ = "merchant"
    name = db.Column(VARCHAR(100), nullable=False)
    phone = db.Column(VARCHAR(15), nullable=True)
    address = db.Column(String)
    hours = db.Column(JSON)

    id = db.Column(GUID, primary_key=True)
    created_time = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_time = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, id: Union[UUID, GUID],
                 name: str, phone: Optional[str],
                 address: str, hours: Dict):
        self.id = id
        self.name = name
        self.phone = phone
        self.address = address
        self.hours = hours
