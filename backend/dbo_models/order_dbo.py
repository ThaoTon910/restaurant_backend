# dbo_models/order_dbo.py
from database import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import VARCHAR, Integer, DateTime, Boolean, Float, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from ._helper import GUID
from dto_models.promotion import  PromotionDTO

class OrderDBO(db.Model):
    __tablename__ = "order"

    id = db.Column(GUID, primary_key=True)
    # foreignkey: look for the id in table "customer" in database
    customer_id = db.Column(GUID, ForeignKey("customer.id"), index=True, nullable=True)
    payment_token = db.Column(VARCHAR(100), nullable=False)
    promo_code = db.Column(VARCHAR(100), nullable=False)
    tax_multiplier = db.Column(Float, nullable=True)
    tip_multiplier = db.Column(Float, nullable=True)
    discount = db.Column(Float, nullable=True)
    status = db.Column(VARCHAR(20), nullable=False)
    created_time = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_time = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    #
    # def __init__(self, dto: PromotionDTO):
    #     self.id = dto.id
    #     self.promotiontype_id = dto.promotiontype_id
    #     self.description = dto.description
    #     self.is_active = dto.is_active
    #     self.start_date = dto.start_date
    #     self.end_date = dto.end_date
    #     self.image_url = dto.image_url
    #     self.promo_code = dto.promo_code
