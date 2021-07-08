from dto_models.menu_item import MenuItemDTO
from dbo_models.menu_item import MenuItemDBO
from services._base import BaseService
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
        return menu_item_dto_to_dbo(dbo)

    def get_all_menu_items(self) -> List[MenuItemDTO]:
        base_query = self.session.query(MenuItemDBO)

        # sort by created_time
        dbos = base_query.order_by( MenuItemDBO.created_time)

        dtos = [menu_item_dbo_to_dto(dbo) for dbo in dbos]
        return dtos

    def get_by_id(self, menu_item_id: UUID) -> MenuItemDTO:
        dbo = self._is_recipe_id_exist(menu_item_id)
        if not dbo:
            raise ObjectNotFound("Recipe id '{}' not found".format(menu_item_id))

        return menu_item_dbo_to_dto(dbo)


