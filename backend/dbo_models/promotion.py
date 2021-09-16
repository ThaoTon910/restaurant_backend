# dbo_models/promotion.py
from database import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import VARCHAR, Integer, DateTime, Boolean, Float, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from ._helper import GUID
from dto_models.promotion import  PromotionDTO

class PromotionDBO(db.Model):
    __tablename__ = "promotion"
    promotion_type = relationship("PromotionTypeDBO", backref="promotion_types")

    id = db.Column(GUID, primary_key=True)
    # foreignkey: look for the id in table "promotiontype" in database
    promotiontype_id = db.Column(GUID, ForeignKey("promotiontype.id"), index=True, nullable=False)
    description = db.Column(VARCHAR(100), nullable=False)
    is_active = db.Column(Boolean, nullable=False)
    start_date = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    end_date = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    created_time = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    image_url = db.Column(String)
    promo_code = db.Column(VARCHAR(25), nullable=False)

    def __init__(self, dto: PromotionDTO):
        self.id = dto.id
        self.promotiontype_id = dto.promotiontype_id
        self.description = dto.description
        self.is_active = dto.is_active
        self.start_date = dto.start_date
        self.end_date = dto.end_date
        self.image_url = dto.image_url
        self.promo_code = dto.promo_code
