# services/promotion_type.py
from dto_models.promotion_type import PromotionTypeDTO
from dbo_models.promotion_type import PromotionTypeDBO
from dbo_models.promotion import PromotionDBO
from converters.promotion_type import promotion_type_dbo_to_dto, promotion_type_dto_to_dbo
from services._base import BaseService
from utils.exceptions import *
from uuid import UUID
from typing import List
import logging

logger = logging.getLogger(__name__)


class PromotionTypeService(BaseService):
    def __init__(self) -> None:
        super().__init__()

    def _is_id_exist(self, promotiontype_id: UUID) -> bool:
        if promotiontype_id is None:
            return False
        return self.session.query(PromotionTypeDBO).filter_by(id=promotiontype_id).first()

    def _is_type_exist(self, type: str) -> bool:
        return self.session.query(PromotionTypeDBO).filter_by(promotion_type=type).first()

    # create new promotion type
    def create(self, dto: PromotionTypeDTO) -> PromotionTypeDTO:
        dbo = promotion_type_dto_to_dbo(dto)
        if self._is_type_exist(dto.promotion_type):
            raise ObjectAlreadyExists(f"Promotion type '{dbo.promotion_type}' already exist")

        self.session.add(dbo)
        self.session.commit()
        return promotion_type_dbo_to_dto(dbo)

    def get_all_promotion_type(self) -> List[PromotionTypeDTO]:
        dbo_list = self.session.query(PromotionTypeDBO).all()
        if not dbo_list:
            raise ObjectNotFound("Promotion type fetch failed")

        return [promotion_type_dbo_to_dto(dbo) for dbo in dbo_list]

    def get_by_id(self, promotiontype_id: UUID) -> PromotionTypeDTO:
        dbo = self.session.query(PromotionTypeDBO).filter_by(id=promotiontype_id).first()
        if not dbo:
            raise ObjectNotFound(f" Id '{promotiontype_id}' not found" )

        return promotion_type_dbo_to_dto(dbo)

    def delete(self, promotiontype_id: UUID) -> PromotionTypeDTO:
        dbo = self.session.query(PromotionTypeDBO).filter_by(id=promotiontype_id).first()
        if not dbo:
            raise ObjectNotFound(f" Try to delete promotion type, but the Id: "
                                 "'{promotiontype_id}' is not found")

        # check if there is any in_active  promotion event
        for db in dbo.promotion_types:
            if db.is_active:
                raise  ChildProcessError(f"FAIL! There is at least one event is still in active mode! "
                                         f"{db.description}")

        #self.session.delete(dbo)
        #self.session.commit()
        return promotion_type_dbo_to_dto(dbo)

    def update(self, dto: PromotionTypeDTO) -> PromotionTypeDTO:
        if dto.id is not None:
            if self._is_id_exist(dto.id):
                dbo = self.session.query(PromotionTypeDBO).filter_by(id=dto.id).first()
                if not dbo:
                    raise ObjectNotFound(f" Id '{dto.id}' not found")

                dbo.promotion_type = dto.promotion_type
                dbo.description = dto.description
                self.session.commit()

                return promotion_type_dbo_to_dto(dbo)
        return None