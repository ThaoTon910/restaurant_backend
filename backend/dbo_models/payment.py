# dbo/payment.py
import uuid
from database import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import VARCHAR,  DateTime, JSON, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from ._helper import GUID
from dto_models.payment import PaymentDTO
from dbo_models.order_dbo import OrderDBO

class PaymentDBO(db.Model):
    __tablename__ = "payment"
    id = db.Column(GUID, primary_key=True, default=uuid.uuid4)
    # foreignkey: look for the id in table "customer" in database

    order = relationship("OrderDBO", backref=backref("payment", cascade="all,delete"))
    order_id = db.Column(GUID, ForeignKey("order.id"), index=True, nullable=True)

    payment_intent_id = db.Column(VARCHAR(100), nullable=False)
    client_secret = db.Column(VARCHAR(100), nullable=False)
    receipt_url = db.Column(VARCHAR(200), nullable=True)
    refunded = db.Column(Boolean, default=False, nullable=False)

    created_time = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_time = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    def __init__(self, payment_intent_id: str, client_secret: str ):
        self.payment_intent_id = payment_intent_id
        self.client_secret = client_secret
