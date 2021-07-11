from dto_models.addon import AddonDTO
from dbo_models.addon import AddonDBO
from converters.addon import addon_dto_to_dbo, addon_dbo_to_dto
from services._base import BaseService
from sqlalchemy import desc
from utils.exceptions import *
from uuid import UUID
from typing import List
import logging

logger = logging.getLogger(__name__)
#create, get_all, get_by_id

class AddonService(BaseService):
    def __init__(self) -> None:
        super().__init__()

    def _is_addon_id_exist(self, id: UUID) -> AddonDBO:
        return self.session.query(AddonDBO).filter_by(id=id).first()

    def _is_addon_name_exist(self, name: str) -> AddonDBO:
        return self.session.query(AddonDBO).filter_by(name=name).first()

    def create(self, dto: AddonDTO) -> AddonDTO:
        dbo = addon_dto_to_dbo(dto)
        # if self._is_addon_name_exist(dto.name):
        #     raise ObjectAlreadyExists("Addon '{}' already exist".format(dbo.name))

        self.session.add(dbo)
        self.session.commit()
        return addon_dbo_to_dto(dbo)

    def get_all_addons(self) -> List[AddonDTO]:
        base_query = self.session.query(AddonDBO)

        # sort by created_time
        dbos = base_query.order_by(AddonDBO.created_time)

        dtos = [addon_dbo_to_dto(dbo) for dbo in dbos]
        return dtos

    def get_addons_from_group(self, group_id: UUID) -> List[AddonDTO]:
        dbo_list = self.session.query(AddonDBO).filter_by(addon_group_id=group_id)\
            .order_by(desc(AddonDBO.created_time))
        if not dbo_list:
            raise ObjectNotFound("Addon fetch failed")
        return [addon_dbo_to_dto(dbo) for dbo in dbo_list]

    def get_by_id(self, addon_id: UUID) -> AddonDTO:
        dbo = self._is_addon_id_exist(addon_id)
        if not dbo:
            raise ObjectNotFound("Addon id '{}' not found".format(addon_id))

        return addon_dbo_to_dto(dbo)