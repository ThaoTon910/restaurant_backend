from dto_models.category import Category as CategoryDTO
from dbo_models.category import Category as CategoryDBO
from services._base import BaseService
from converters.category import category_dbo_to_dto, category_dto_to_dbo
from utils.exceptions import *
from uuid import UUID
from typing import List
import logging

logger = logging.getLogger(__name__)


class CategoryService(BaseService):
    def __init__(self) -> None:
        super().__init__()

    def _is_category_id_exist(self, id: UUID) -> CategoryDBO:
        return self.session.query(CategoryDBO).filter_by(id=id).first()

    def _is_category_name_exist(self, name: str) -> bool:
        return self.session.query(CategoryDBO).filter_by(name=name).first()

    def create(self, dto: CategoryDTO) -> CategoryDTO:
        dbo = category_dto_to_dbo(dto)
        if self._is_category_name_exist(dto.name):
            raise ObjectAlreadyExists("Category '{}' already exist".format(dbo.name))

        self.session.add(dbo)
        self.session.commit()
        return category_dbo_to_dto(dbo)

    def get_by_id(self, category_id: UUID) -> CategoryDTO:
        dbo = self.session.query(CategoryDBO).filter_by(id=category_id).first()
        if not dbo:
            raise ObjectNotFound("Category id '{}' not found".format(category_id))

        return category_dbo_to_dto(dbo)


