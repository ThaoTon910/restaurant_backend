# dbo_models/extra_percentage_all.py
from database import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import VARCHAR, Integer, DateTime, Boolean, Float, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from ._helper import GUID
from dto_models.extra_percentage_all import  ExtraPercentageAllDTO


class ExtraPercentageAllDBO(db.Model):
    __tablename__ = "extrapercentageall"
    promotion_type = relationship("PromotionTypeDBO", backref="extra_pa")

    id = db.Column(GUID, primary_key=True)
    # foreignkey: look for the id in table "promotiontype" in database
    promotiontype_id = db.Column(GUID, ForeignKey("promotiontype.id"), index=True, nullable=False)
    percent_off = db.Column(Float, nullable=False)
    updated_time = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    def __init__(self, dto: ExtraPercentageAllDTO):
        self.id = dto.id
        self.promotiontype_id = dto.promotiontype_id
        self.percent_off = dto.percent_off
