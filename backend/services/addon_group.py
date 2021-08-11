from dto_models.addon_group import AddonGroupDTO
from dbo_models.addon_group import AddonGroupDBO
from dbo_models.menu_item_to_addon_group import MenuItemToAddonGroupDBO
from converters.addon_group import addon_group_dto_to_dbo, addon_group_dbo_to_dto
from services._base import BaseService
from sqlalchemy import desc
from flask import abort
from utils.exceptions import *
from uuid import UUID
import logging
from typing import List

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
        dbo = addon_group_dto_to_dbo(dto)
        if self._is_addon_group_name_exist(dto.name):
            raise ObjectAlreadyExists("Addon Group '{}' already exist".format(dbo.name))
        self.session.add(dbo)
        self.session.commit()
        return addon_group_dbo_to_dto(dbo)

    def get_all_addon_groups(self) -> List[AddonGroupDTO]:
        dbo_list = self.session.query(AddonGroupDBO).all()
        return [addon_group_dbo_to_dto(dbo) for dbo in dbo_list]

    def get_addon_groups_from_menu_item(self, menu_item_id: UUID) -> List[AddonGroupDTO]:
        #In MenuItemToAddonGroup Table, take all rows that have menu item id = input
        menu_item_to_addon_group_dbos: List[MenuItemToAddonGroupDBO] = self.session.query(MenuItemToAddonGroupDBO).filter(MenuItemToAddonGroupDBO.menu_item_id==menu_item_id)
        addon_group_ids = [item.addon_group_id for item in menu_item_to_addon_group_dbos] # get ids only [id1, id2]
        # l = []
        # for item in menu_item_to_addon_group_dbos:
        #     l.append(item.addon_group_id)

        #In Addon Group table, get all rows that have id in addon_group_ids
        dbo_list = self.session.query(AddonGroupDBO).filter(AddonGroupDBO.id.in_(addon_group_ids))\
            .order_by(desc(AddonGroupDBO.min_quantity)) # mandatory group need to be first
        if not dbo_list:
            raise ObjectNotFound("Addon Group fetch failed")
        return [addon_group_dbo_to_dto(dbo) for dbo in dbo_list]

    def get_by_id(self,addon_group_id: UUID)-> AddonGroupDTO:
        dbo = self.session.query(AddonGroupDBO).filter_by(id=addon_group_id).first()
        if not dbo:
            raise ObjectNotFound("Addon Group '{}' not found".format(addon_group_id))
        return addon_group_dbo_to_dto(dbo)

    # #Delete all
    # def delete_all(self):
    #     dbo_list = self.session.query(AddonGroupDBO).all()
    #     if not dbo_list:
    #         raise ObjectNotFound("Addon Group fetch failed")
    #     self.session.delete(dbo_list)  # delete addon group bu id
    #     self.session.commit()  # save to database
    #     return [addon_group_dbo_to_dto(dbo) for dbo in dbo_list]

    # #Delete by id
    # def delete(self, addon_group_id:UUID)-> AddonGroupDTO:
    #     dbo = self.session.query(AddonGroupDBO).filter_by(id=addon_group_id).first()
    #     if not dbo:
    #         raise ObjectNotFound("Addon Group '{}' not found".format(addon_group_id))
    #     self.session.delete(dbo) #delete addon group by id
    #     self.session.commit() #save to database
    #     return addon_group_dbo_to_dto(dbo)

    #Update
    def update(self, dto: AddonGroupDTO) -> AddonGroupDTO:
        dbo = addon_group_dto_to_dbo(dto)
        r = self.session.query(AddonGroupDBO).filter(AddonGroupDBO.id == dto.id).update(self.get_updated_key_value(dbo))
        self.session.commit()
        return self.get_by_id(dto.id)

    #Delete
    def delete(self, addon_group_id: UUID) -> AddonGroupDTO:
        dbo = self.session.query(AddonGroupDBO).filter_by(id=addon_group_id).first()
        if not dbo:
            raise ObjectNotFound("Add on group id '{}' not found".format(addon_group_id))
        dto: AddonGroupDTO = addon_group_dbo_to_dto(dbo)
        if len(dto.addons) > 0:
            raise InvalidOperation("Please delete all addons under {} first".format(dto.name))
        #delete
        self.session.delete(dbo)
        #save the database
        self.session.commit()
        #return the deleted addon group
        return dto
