from dto_models.merchant import MerchantDTO
from dbo_models.merchant import MerchantDBO
from services._base import BaseService
from converters.merchant import merchant_dbo_to_dto, merchant_dto_to_dbo
from typing import List
from utils.exceptions import *
from uuid import UUID
import logging

logger = logging.getLogger(__name__)


class MerchantService(BaseService):
    def __init__(self) -> None:
        super().__init__()

    def _is_category_id_exist(self, id: UUID) -> MerchantDBO:
        return self.session.query(MerchantDBO).filter_by(id=id).first()

    def _is_category_name_exist(self, name: str) -> bool:
        return self.session.query(MerchantDBO).filter_by(name=name).first()

    # Outcome: input from Resource (DTO) -> output send back to the UI (DTO) too
    # We use the Convertes to convert dto to DBO and then, add and commit to database
    # Then, we return the Convertes to convert dbo to DTO
    def create(self, dto: MerchantDTO) -> MerchantDTO:
        dbo = merchant_dto_to_dbo(dto)
        if self._is_category_name_exist(dto.name):
            raise ObjectAlreadyExists("Merchant '{}' already exist".format(dbo.name))

        self.session.add(dbo)
        self.session.commit()
        return self.get_by_id(dto.id)

    # We get all categories from database (DBO) -> return DT
    # We use the ".query" in DBO database to get all
    def get_all_merchants(self) -> List[MerchantDTO]:
        dbo_list = self.session.query(MerchantDBO).all()
        return [merchant_dbo_to_dto(dbo) for dbo in dbo_list]

    def get_by_id(self, category_id: UUID) -> MerchantDTO:
        dbo = self.session.query(MerchantDBO).filter_by(id=category_id).first()
        if not dbo:
            raise ObjectNotFound("Merchant id '{}' not found".format(category_id))
        return merchant_dbo_to_dto(dbo)

    def update(self, dto: MerchantDTO) -> MerchantDTO:
        dbo = merchant_dto_to_dbo(dto)
        r = self.session.query(MerchantDBO).filter(MerchantDBO.id == dto.id).update(self.get_updated_key_value(dbo))
        # self.session.merge(dbo)
        self.session.commit()
        return self.get_by_id(dto.id)

    def delete(self, mechant_id: UUID) -> MerchantDTO:
        #find merchant by id
        dbo = self.session.query(MerchantDBO).filter_by(id=mechant_id).first()
        if not dbo:
            raise ObjectNotFound("merchant id '{}' not found".format(mechant_id))
        dto: MerchantDTO = merchant_dbo_to_dto(dbo)
        if not dbo:
            raise ObjectNotFound("merchant id id '{}' not found".format(mechant_id))
        #delete the merchant
        self.session.delete(dbo)
        #save the database
        self.session.commit()
        #return the deleted category
        return dto
