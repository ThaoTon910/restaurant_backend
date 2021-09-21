# dbo_models/order_dbo.py
from database import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import VARCHAR,  DateTime, JSON, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ._helper import GUID
from dto_models.app_order_dto import OrderDTO

class OrderDBO(db.Model):
    __tablename__ = "order"

    id = db.Column(GUID, primary_key=True)
    # foreignkey: look for the id in table "customer" in database
    customer_id = db.Column(GUID, ForeignKey("customer.id"), index=True, nullable=True)
    customer = relationship("CustomerDBO", backref="orders")
    payment_token = db.Column(VARCHAR(100), nullable=False)
    promo_code = db.Column(VARCHAR(100), nullable=False)
    tax_multiplier = db.Column(Float, nullable=True)
    tip_multiplier = db.Column(Float, nullable=True)
    discount = db.Column(Float, nullable=True)
    status = db.Column(VARCHAR(20), nullable=False)
    created_time = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_time = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    def __init__(self, dto: OrderDTO):
        self.status = "pending"
        self.payment_token = dto.payment_token
        self.promo_code = dto.promo_code
        self.discount = 0
        self.tip_multiplier = dto.tip_multiplier
        self.tax_multiplier = dto.tax_multiplier
        self.id = dto.id
