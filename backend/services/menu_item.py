from dto_models.menu_item import MenuItemDTO
from dbo_models.menu_item import MenuItemDBO
from dto_models.addon_group import AddonGroupDTO
from services._base import BaseService
from services.addon_group import AddonGroupService
from sqlalchemy import desc
from converters.menu_item import menu_item_dbo_to_dto, menu_item_dto_to_dbo
from utils.exceptions import *
from uuid import UUID
from typing import List
import logging

logger = logging.getLogger(__name__)
#create, get_by_id, get_all, update, delete
class MenuItemService(BaseService):
    def __init__(self) -> None:
        super().__init__()

    def _is_recipe_id_exist(self, id: UUID) -> MenuItemDBO:
        return self.session.query(MenuItemDBO).filter_by(id=id).first()

    def _is_recipe_name_exist(self, name: str) -> MenuItemDBO:
        return self.session.query(MenuItemDBO).filter_by(name=name).first()

    def create(self, dto: MenuItemDTO) -> MenuItemDTO:
        dbo = menu_item_dto_to_dbo(dto)
        if self._is_recipe_name_exist(dto.name):
            raise ObjectAlreadyExists("Recipe '{}' already exist".format(dbo.name))

        self.session.add(dbo)
        self.session.commit()
        # return menu_item_dto_to_dbo(dbo)
        return menu_item_dbo_to_dto(dbo)


    def get_all_menu_items(self) -> List[MenuItemDTO]:
        base_query = self.session.query(MenuItemDBO)

        # sort by created_time
        dbos = base_query.order_by(MenuItemDBO.created_time)
        dtos = [menu_item_dbo_to_dto(dbo) for dbo in dbos]
        # addon_group_service = AddonGroupService()
        # for dto in dtos:
        #     addon_groups: List[AddonGroupDTO] = addon_group_service.get_addon_groups_from_menu_item(dto.id)
        #     dto.addon_group_ids = [addon_group.id for addon_group in addon_groups]
        return dtos

    def get_menu_items_from_category(self, category_id: UUID) -> List[MenuItemDTO]:
        dbo_list = self.session.query(MenuItemDBO).filter(MenuItemDBO.category_id==category_id)\
            .order_by(desc(MenuItemDBO.created_time))
        if not dbo_list:
            raise ObjectNotFound("Menu Items fetch failed")
        dtos = [menu_item_dbo_to_dto(dbo) for dbo in dbo_list]

        addon_group_service = AddonGroupService()
        for dto in dtos:
            addon_groups: List[AddonGroupDTO] = addon_group_service.get_addon_groups_from_menu_item(dto.id)
            dto.addon_group_ids = [addon_group.id for addon_group in addon_groups]

        return dtos

    def get_by_id(self, menu_item_id: UUID) -> MenuItemDTO:
        dbo = self._is_recipe_id_exist(menu_item_id)
        if not dbo:
            raise ObjectNotFound("Recipe id '{}' not found".format(menu_item_id))
        dto: MenuItemDTO = menu_item_dbo_to_dto(dbo)

        # # TODO: optimize query to join data across table
        # addon_groups: List[AddonGroupDTO] = AddonGroupService().get_addon_groups_from_menu_item(dto.id)
        #
        # dto.addon_group_ids= [addon_group.id for addon_group in addon_groups]

        return dto


