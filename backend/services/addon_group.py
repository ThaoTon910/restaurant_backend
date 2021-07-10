from dto_models.addon_group import AddonGroupDTO
from dbo_models.addon_group import AddonGroupDBO
from converters.addon_group import addon_dto_to_dbo, addon_dbo_to_dto
from services._base import BaseService
from utils.exceptions import *
from uuid import UUID
import logging

logger = logging.getLogger(__name__)
#create(post), get_by_id, get_all, update, delete

class AddonGroupService(BaseService):
    def __init__(self) -> None:
        super().__init__()

    def _is_addon_group_id_exist(self, id: UUID) -> AddonGroupDBO:
        return self.session.query(AddonGroupDBO).filter_by(id=id).first()

    def _is_addon_group_name_exist(self, name: str) -> bool:
        return self.session.query(AddonGroupDBO).filter_by(name=name).first()


    def create(self, dto:AddonGroupDTO) -> AddonGroupDTO:
        dbo = addon_dto_to_dbo(dto)
        if self._is_addon_group_name_exist(dto.name):
            raise ObjectAlreadyExists("Addon Group '{}' already exist".format(dbo.name))
        self.session.add(dbo)
        self.session.commit()
        return addon_dbo_to_dto(dbo)

    def get_all_addon_groups(self):
        dbo_list = self.session.query(AddonGroupDBO).all()
        if not dbo_list:
            raise ObjectNotFound("Addon Group fetch failed")
        return [addon_dbo_to_dto(dbo) for dbo in dbo_list]

    def get_by_id(self,addon_group_id: UUID)-> AddonGroupDTO:
        dbo = self.session.query(AddonGroupDBO).filter_by(id=addon_group_id).first()
        if not dbo:
            raise ObjectNotFound("Addon Group '{}' not found".format(addon_group_id))
        return addon_dbo_to_dto(dbo)

    #Delete all
    def delete_all_addon_groups(self):
        dbo_list = self.session.query(AddonGroupDBO).all()
        if not dbo_list:
            raise ObjectNotFound("Addon Group fetch failed")
        self.session.delete(dbo_list)  # delete addon group bu id
        self.session.commit()  # save to database
        return [addon_dbo_to_dto(dbo) for dbo in dbo_list]

    #Delete by id
    def delete_addon_group_id(self, addon_group_id:UUID)-> AddonGroupDTO:
        dbo = self.session.query(AddonGroupDBO).filter_by(id=addon_group_id).first()
        if not dbo:
            raise ObjectNotFound("Addon Group '{}' not found".format(addon_group_id))
        self.session.delete(dbo) #delete addon group by id
        self.session.commit() #save to database
        return addon_dbo_to_dto(dbo)

    #Update
    def update_addon_group(self, dto: AddonGroupDTO) -> AddonGroupDTO:
        dbo = self.session.query(AddonGroupDBO).filter_by(id=dto.id).first()
        if not dbo:
            raise ObjectNotFound("Category id '{}' not found".format(dbo.id))
        dbo.name = dto.name
        dbo.max_quantity = dto.max_quantity
        dbo.mix_quantity = dto.min_quantity
        self.session.commit()
        return addon_dbo_to_dto(dbo)
