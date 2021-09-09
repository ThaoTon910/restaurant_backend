# services/order_service.py
from services._base import BaseService
from utils.exceptions import *
from uuid import UUID
from typing import List
from dbo_models.menu_item import MenuItemDBO
from dto_models.app_order_dto import OrderDTO
from dbo_models.addon import AddonDBO
from dbo_models.order_dbo import OrderDBO
from dbo_models.order_item import OrderItemDBO
from dbo_models.add_on_to_order_item import AddonToOrderItem
from dbo_models.customer import CustomerDBO




import logging

logger = logging.getLogger(__name__)

# working with database, and logic
class OrderService(BaseService):
    def __init__(self) -> None:
        super().__init__()



    # def _is_id_exist(self, promotion_id: UUID) -> bool:
    #     return self.session.query(PromotionDBO).filter_by(id=promotion_id).first()

    # create new promotion in table "promotion", get data from resource
    def create(self, dto: OrderDTO) -> OrderDTO:
        # dbo = promotion_dto_to_dbo(dto)
        # if self._is_id_exist(dto.id):
        #     raise ObjectAlreadyExists(f"This promotion ID '{dbo.id}' already exist" )
        # if self._is_duplicate(dbo.promo_code):
        #     raise ObjectAlreadyExists(f"This promotion code '{dbo.promo_code}' is in active"
        #                               f"Description: {dbo.description} .")

        # self.session.add(dbo)
        # self.session.commit()
        # return promotion_dbo_to_dto(dbo)

        for item in dto.items:
            item_dbo = self.session.query(MenuItemDBO).get(item["menu_item_id"])
            print("item dbo: ", item_dbo)
            price = item_dbo.price
            for addon in item["add_ons"]:
                add_on_dbo = self.session.query(AddonDBO).get(addon)
                print("add_on dbo: ", add_on_dbo)
                price += add_on_dbo.price
            print("price: ", price)

        return dto