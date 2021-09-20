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

    def _is_merchant_id_exist(self, id: UUID) -> MerchantDBO:
        return self.session.query(MerchantDBO).filter_by(id=id).first()

    def _is_merchant_name_exist(self, name: str) -> bool:
        return self.session.query(MerchantDBO).filter_by(name=name).first()

    # Outcome: input from Resource (DTO) -> output send back to the UI (DTO) too
    # We use the Convertes to convert dto to DBO and then, add and commit to database
    # Then, we return the Convertes to convert dbo to DTO
    def create(self, dto: MerchantDTO) -> MerchantDTO:
        dbo = merchant_dto_to_dbo(dto)
        if self._is_merchant_name_exist(dto.name):
            raise ObjectAlreadyExists("Merchant '{}' already exist".format(dbo.name))
        self.session.add(dbo)
        self.session.commit()
        return merchant_dbo_to_dto(dbo)

    # We get all categories from database (DBO) -> return DT
    # We use the ".query" in DBO database to get all
    def get_merchant(self) -> List[MerchantDTO]:
        dbo = self.session.query(MerchantDBO).first()
        if not dbo:
            raise ObjectNotFound("merchant not found")
        return merchant_dbo_to_dto(dbo)

    def update(self, dto: MerchantDTO) -> MerchantDTO:
        dbo = merchant_dto_to_dbo(dto)
        dbo2 = self.session.query(MerchantDBO).first()
        # ToDo: remove merchant id
        r = self.session.query(MerchantDBO).filter(MerchantDBO.id == dbo2.id).update(self.get_updated_key_value(dbo))
        # self.session.merge(dbo)
        self.session.commit()
        return merchant_dbo_to_dto(dbo)

    def delete(self) -> MerchantDTO:
        #find merchant
        dbo = self.session.query(MerchantDBO).first()
        if not dbo:
            raise ObjectNotFound("merchant not found")
        dto: MerchantDTO = merchant_dbo_to_dto(dbo)
        #delete the merchant
        self.session.delete(dbo)
        #save the database
        self.session.commit()
        #return the deleted category
        return dto
