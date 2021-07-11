
from services._base import BaseService
from dto_models.menu import MenuDTO
from services.category import CategoryService
from services.addon_group import AddonGroupService
from sqlalchemy import desc
from utils.exceptions import *
from uuid import UUID
from typing import List
import logging

logger = logging.getLogger(__name__)
#create, get_by_id, get_all, update, delete
class MenuService(BaseService):


    def get_menu(self) -> MenuDTO:
        category_service = CategoryService()
        addon_group_service = AddonGroupService()
        categories = category_service.get_all_categories()
        addon_groups = addon_group_service.get_all_addon_groups()
        menu = MenuDTO(categories=categories, addon_groups=addon_groups)
        return menu


