# services/promotion.py
from dto_models.promotion import PromotionDTO
from dbo_models.promotion import PromotionDBO
from converters.promotion import promotion_dbo_to_dto, promotion_dto_to_dbo
from services._base import BaseService
from utils.exceptions import *
from uuid import UUID
from typing import List
import logging

logger = logging.getLogger(__name__)

# working with database, and logic
class PromotionService(BaseService):
    def __init__(self) -> None:
        super().__init__()

    def _is_id_exist(self, promotion_id: UUID) -> bool:
        return self.session.query(PromotionDBO).filter_by(id=promotion_id).first()

    # check duplicate in active promo code
    def _is_duplicate(self, promo_code: str) -> bool:
        active_list = self.session.query(PromotionDBO).filter_by(promo_code=promo_code).all()
        if active_list is not None:
            for pc in  active_list:
                if  pc.is_active:
                    return True
        return False

    # create new promotion in table "promotion", get data from resource
    def create(self, dto: PromotionDTO) -> PromotionDTO:
        dbo = promotion_dto_to_dbo(dto)
        if self._is_id_exist(dto.id):
            raise ObjectAlreadyExists(f"This promotion ID '{dbo.id}' already exist" )
        if self._is_duplicate(dbo.promo_code):
            raise ObjectAlreadyExists(f"This promotion code '{dbo.promo_code}' is in active"
                                      f"Description: {dbo.description} .")

        self.session.add(dbo)
        self.session.commit()
        return promotion_dbo_to_dto(dbo)

    # get the list of all promotions in table "promotion"
    def get_all_promotion(self) -> List[PromotionDTO]:
        dbo_list = self.session.query(PromotionDBO).order_by(PromotionDBO.created_time.desc()).all()
        if not dbo_list:
            raise ObjectNotFound("Promotion type fetch failed")

        # return the list in dto format
        return [promotion_dbo_to_dto(dbo) for dbo in dbo_list]

    # get a promotion by ID
    def get_by_id(self, promotion_id: UUID) -> PromotionDTO:
        dbo = self.session.query(PromotionDBO).filter_by(id=promotion_id).first()
        if not dbo:
            raise ObjectNotFound(f" Promotion Id '{promotion_id}' not found!")
        # return  an object in dto format
        return promotion_dbo_to_dto(dbo)

    # delete a promotion by ID
    def delete(self, promotion_id: UUID) -> PromotionDTO:
        dbo = self.session.query(PromotionDBO).filter_by(id=promotion_id).first()
        if not dbo:
            raise ObjectNotFound(f" Try to delete promotion type, but the Id: "
                                 f"'{promotion_id}' is not found")
        self.session.delete(dbo)
        self.session.commit()
        # return the deleted object
        return promotion_dbo_to_dto(dbo)

    # update promotion info or PROMO CODE
    def update(self, dto: PromotionDTO) -> PromotionDTO:
        print(f"test UPDATE {dto.id}\n")
        if self._is_id_exist(dto.id):
            print("test UPDATE 2 ====\n")
            dbo = self.session.query(PromotionDBO).filter_by(id=dto.id).first()
            if not dbo:
                raise ObjectNotFound(f" Id '{dto.id}' not found")
            if dbo.promotiontype_id != dto.promotiontype_id:
                raise ObjectNotFound(f"Can not change the type of this promotion. "
                                     f"Please create a new one in the correct promotion type ")
            dbo.promo_code = dto.promo_code
            dbo.description = dto.description
            dbo.is_active = dto.is_active
            dbo.start_date = dto.start_date
            dbo.end_date = dto.end_date
            dbo.image_url = dto.image_url
            self.session.commit()
            return promotion_dbo_to_dto(dbo)
