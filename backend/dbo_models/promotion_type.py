from database import db
from sqlalchemy import VARCHAR, Integer, DateTime
from datetime import datetime
from dto_models.promotion_type import PromotionTypeDTO
from ._helper import GUID

class PromotionTypeDBO(db.Model):
    __tablename__ = "promotiontype"
    promotion_type = db.Column(VARCHAR(100), nullable=False)
    description = db.Column(VARCHAR(100), nullable=False)
    id = db.Column(GUID, primary_key=True)
    created_time = db.Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow())

    def __init__(self, dto: PromotionTypeDTO):
        self.id = dto.id
        self.promotion_type = dto.promotion_type.strip()
        self.description = dto.description

