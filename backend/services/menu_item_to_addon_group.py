from dto_models.menu_item_to_addon_group import MenuItemToAddonGroupDTO
from dbo_models.menu_item_to_addon_group import MenuItemToAddonGroupDBO
from converters.menu_item_to_addon_group import menu_item_to_addon_group_dbo_to_dto, menu_item_to_addon_group_dto_to_dbo
from services._base import BaseService
from utils.exceptions import *
from uuid import UUID
from sqlalchemy import and_
from typing import List
import logging

logger = logging.getLogger(__name__)

#create, get_all, get_by_id, update, delete
class MenuItemToAddonGroupService(BaseService):
    def __init__(self) -> None:
        super().__init__()

    def _is_menu_item_to_addon_group_id_exist(self, id: UUID) -> MenuItemToAddonGroupDBO:
        return self.session.query(MenuItemToAddonGroupDBO).filter_by(id=id).first()

    def _is_menu_item_to_addon_group_name_exist(self, name: str) -> bool:
        return self.session.query(MenuItemToAddonGroupDBO).filter_by(name=name).first()

    def create(self, dto:MenuItemToAddonGroupDTO) -> MenuItemToAddonGroupDTO:
        dbo = menu_item_to_addon_group_dto_to_dbo(dto)
        self.session.add(dbo)
        self.session.commit()
        return menu_item_to_addon_group_dbo_to_dto(dbo)

    def get_all_addon_groups(self):
        dbo_list = self.session.query(MenuItemToAddonGroupDBO).all()
        if not dbo_list:
            raise ObjectNotFound("Menu Item to Addon Group fetch failed")
        return [menu_item_to_addon_group_dbo_to_dto(dbo) for dbo in dbo_list]

    def delete(self, menu_item_id: UUID, addon_group_id: UUID) -> MenuItemToAddonGroupDTO:
        #find menu item to addon group
        dbo = self.session.query(MenuItemToAddonGroupDBO).filter(and_(MenuItemToAddonGroupDBO.menu_item_id==menu_item_id, MenuItemToAddonGroupDBO.addon_group_id==addon_group_id)).first()
        if not dbo:
            raise ObjectNotFound("MenuItemToAddonGroup id '{}' not found".format())
        dto: MenuItemToAddonGroupDTO = menu_item_to_addon_group_dbo_to_dto(dbo)
        #delete menu item to addon group
        self.session.delete(dbo)
        #save the database
        self.session.commit()
        #return the deleted menu item to addon group
        return dto

    # def get_by_id(self,addon_group_id: UUID)-> MenuItemToAddonGroupDTO:
    #     dbo = self.session.query(MenuItemToAddonGroupDBO).filter_by(id=).first()
    #     if not dbo:
    #         raise ObjectNotFound("Menu Item to Addon Group '{}' not found".format(addon_group_id))
    #     return menu_item_to_addon_group_dbo_to_dto(dbo)
