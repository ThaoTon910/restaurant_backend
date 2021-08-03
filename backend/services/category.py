from dto_models.category import CategoryDTO
from dbo_models.category import CategoryDBO
from dto_models.menu_item import MenuItemDTO
from services.menu_item import MenuItemService
from converters.category import category_dbo_to_dto, category_dto_to_dbo
from services._base import BaseService
from utils.exceptions import *
from uuid import UUID
from typing import List
import logging

logger = logging.getLogger(__name__)

#create, get_all, get_by_id, update, delete
class CategoryService(BaseService):
    def __init__(self) -> None:
        super().__init__()

    def _is_category_id_exist(self, id: UUID) -> CategoryDBO:
        return self.session.query(CategoryDBO).filter_by(id=id).first()

    def _is_category_name_exist(self, name: str) -> bool:
        return self.session.query(CategoryDBO).filter_by(name=name).first()

    # Outcome: input from Resource (DTO) -> output send back to the UI (DTO) too
    # We use the Convertes to convert dto to DBO and then, add and commit to database
    # Then, we return the Convertes to convert dbo to DTO
    def create(self, dto: CategoryDTO) -> CategoryDTO:
        dbo = category_dto_to_dbo(dto)
        if self._is_category_name_exist(dto.name):
            raise ObjectAlreadyExists("Category '{}' already exist".format(dbo.name))

        self.session.add(dbo)
        self.session.commit()
        return self.get_by_id(dto.id)

    # We get all categories from database (DBO) -> return DT
    # We use the ".query" in DBO database to get all
    def get_all_categories(self) -> List[CategoryDTO]:
        dbo_list = self.session.query(CategoryDBO).all()
        menu_item_service = MenuItemService()
        if not dbo_list:
            raise ObjectNotFound("Categories fetch failed")

        return [category_dbo_to_dto(dbo) for dbo in dbo_list]

    def get_by_id(self, category_id: UUID) -> CategoryDTO:
        dbo = self.session.query(CategoryDBO).filter_by(id=category_id).first()
        if not dbo:
            raise ObjectNotFound("Category id '{}' not found".format(category_id))
        # dto: CategoryDTO = category_dbo_to_dto(dbo)
        #
        # # TODO: optimize query to join data across table
        # menu_items: List[MenuItemDTO] = MenuItemService().get_menu_items_from_category(dto.id)
        # dto.menu_items = menu_items
        return category_dbo_to_dto(dbo)

    def update(self, dto: CategoryDTO) -> CategoryDTO:
        dbo = category_dto_to_dbo(dto)
        r = self.session.query(CategoryDBO).filter(CategoryDBO.id == dto.id).update(self.get_updated_key_value(dbo))
        # self.session.merge(dbo)
        self.session.commit()
        return self.get_by_id(dto.id)

    def delete(self, category_id: UUID) -> CategoryDTO:
        #find category by id
        dbo = self.session.query(CategoryDBO).filter_by(id=category_id).first()
        if not dbo:
            raise ObjectNotFound("Category id '{}' not found".format(category_id))
        #delete the category
        self.session.delete(dbo)
        #save the database
        self.session.commit()
        #return the deleted category
        return category_dbo_to_dto(dbo)
