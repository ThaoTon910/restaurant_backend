# services/extra_percentage_all.py
from dto_models.extra_percentage_all import ExtraPercentageAllDTO
from dbo_models.extra_percentage_all import ExtraPercentageAllDBO
from converters.extra_percentage_all import extra_percentage_all_dbo_to_dto, extra_percentage_all_dto_to_dbo
from services._base import BaseService
from utils.exceptions import *
from uuid import UUID
from typing import List
import logging

logger = logging.getLogger(__name__)

# working with database, and logic
class ExtraPercentageAllService(BaseService):
    def __init__(self) -> None:
        super().__init__()

    def _is_id_exist(self, promotion_id: UUID) -> bool:
        return self.session.query(ExtraPercentageAllDBO).filter_by(id=promotion_id).first()


    def get_percent_off(self) -> float:
        dbo = self.session.query(ExtraPercentageAllDBO).first()
        if not dbo:
            raise ObjectNotFound("Promotion type fetch failed")
        percent_off = dbo.percent_off
        # return the list in dto format
        return percent_off

    # create new extra percentage off
    def create(self, dto: ExtraPercentageAllDTO) -> ExtraPercentageAllDTO:
        dbo = extra_percentage_all_dto_to_dbo(dto)
        if self._is_id_exist(dto.id):
            raise ObjectAlreadyExists(f"This promotion has already existed. Delete or edit the current one!")
        is_empty = self.session.query(ExtraPercentageAllDBO).all()
        if not is_empty:
            self.session.add(dbo)
            self.session.commit()
            return extra_percentage_all_dbo_to_dto(dbo)
        else:
            raise ObjectAlreadyExists(f"Table is not empty!")

    def get_all(self) -> List[ExtraPercentageAllDTO]:
        dbo_list = self.session.query(ExtraPercentageAllDBO).order_by(ExtraPercentageAllDBO.percent_off.desc()).all()
        if not dbo_list:
            raise ObjectNotFound("Promotion type fetch failed")

        # return the list in dto format
        return [extra_percentage_all_dbo_to_dto(dbo) for dbo in dbo_list]

    def get_by_id(self, extra_id: UUID) -> ExtraPercentageAllDTO:
        dbo = self.session.query(ExtraPercentageAllDBO).filter_by(id=extra_id).first()
        if not dbo:
            raise ObjectNotFound(f" Promotion Id '{extra_id}' is not found!")
        # return  an object in dto format
        return extra_percentage_all_dbo_to_dto(dbo)

    # delete a promotion by ID
    def delete(self, extra_id: UUID) -> ExtraPercentageAllDTO:
        dbo = self.session.query(ExtraPercentageAllDBO).filter_by(id=extra_id).first()
        if not dbo:
            raise ObjectNotFound(f" Try to delete promotion type, but the Id: "
                                 f"'{extra_id}' is not found")
        self.session.delete(dbo)
        self.session.commit()
        # return the deleted object
        return extra_percentage_all_dbo_to_dto(dbo)

        # update promotion info or PROMO CODE

    def update(self, dto: ExtraPercentageAllDTO) -> ExtraPercentageAllDTO:
        if self._is_id_exist(dto.id):
            dbo = self.session.query(ExtraPercentageAllDBO).filter_by(id=dto.id).first()
            if not dbo:
                raise ObjectNotFound(f" Id '{dto.id}' not found")

            dbo.percent_off = dto.percent_off
            dbo.updated_time = dto.updated_time
            self.session.commit()
            return extra_percentage_all_dbo_to_dto(dbo)
        else:
            return None
