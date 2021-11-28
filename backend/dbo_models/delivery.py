# dbo_models/delivery.py
import uuid
from database import db
from sqlalchemy import VARCHAR, Integer, DateTime, Float, ForeignKey
from datetime import datetime
from ._helper import GUID
from sqlalchemy.orm import relationship, backref

class PickUpDBO(db.Model):
    __tablename__ = "pickup"
    time = db.Column(DateTime(timezone=True), nullable=False)
    merchant = relationship("MerchantDBO", backref=backref("pick_up", cascade="all,delete"))
    merchant_id = db.Column(GUID, ForeignKey("merchant.id"),  nullable=False)

    id = db.Column(GUID, primary_key=True, default=uuid.uuid4)



class DeliveryDBO(db.Model):
    __tablename__ = "delivery"
    fee = db.Column(Float, nullable=False)
    pick_up = relationship("PickUpDBO", backref=backref("delivery", cascade="all,delete"))
    pick_up_id = db.Column(GUID, ForeignKey("pickup.id"),  nullable=True)
    delivery_type = db.Column(VARCHAR(50), nullable=False)

    order = relationship("OrderDBO", backref=backref("delivery", cascade="all,delete"))
    order_id = db.Column(GUID, ForeignKey("order.id"), nullable=True)

    id = db.Column(GUID, primary_key=True, default=uuid.uuid4)
    created_time = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow())

    def __init__(self, delivery_type: str, fee: float, time, merchant_id: uuid ):
        self.delivery_type = delivery_type
        self.fee = fee
        if delivery_type == "pickup":
            pick_up_new = PickUpDBO(time=time, merchant_id=merchant_id)
            self.pick_up = pick_up_new

