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
from converters.order_convert import order_dbo_to_dto
from dbo_models.delivery import DeliveryDBO
from dto_models.payment_intent import PaymentIntentDTO
import stripe

stripe.api_key = "sk_test_51JntlwGjZM1U6lN0oZsX1AREl2jMAfbhPcrE26o9dNNokPvIbakkKgtF2C67RZdb9fP7KbVueacZq1I23hREErdJ00Sp1BXXYs"

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
        print("inside service 1")

        order_dbo = OrderDBO(dto)

        customer_dbo = CustomerDBO(first_name=dto.customer["first_name"],
                                   last_name=dto.customer["last_name"],
                                   email=dto.customer["email"],
                                   phone_number=dto.customer["phone_number"])
        order_dbo.customer = customer_dbo

        delivery = DeliveryDBO(delivery_type=dto.delivery["info"]["delivery_type"],
                               fee=dto.delivery["delivery_fee"],
                               time=dto.delivery["info"]["time"],
                               merchant_id=dto.delivery["info"]["merchant_id"])
        # order_dbo.delivery.append

        delivery.order = order_dbo
        order_dbo.discount=0.0

        for item in dto.items:
            item_dbo = self.session.query(MenuItemDBO).get(item["menu_item_id"])
            print("item dbo: ", item_dbo)
            price = item_dbo.price
            order_item_dbo = OrderItemDBO(order=order_dbo, menu_item=item_dbo, quantity=item["quantity"],
                                          special_instruction=item["special_instruction"])
            if "add_ons" in  item:
                for addon in item["add_ons"]:
                    add_on_dbo = self.session.query(AddonDBO).get(addon)
                    print("add_on dbo: ", add_on_dbo)
                    price += add_on_dbo.price
                    order_item_dbo.add_ons.append(add_on_dbo)
                # print("price: ", price)

            order_item_dbo.price = price #*item["quantity"]
            # order_dbo.order_items.append(order_item_dbo)

        # print("order_dbo return:", order_dbo.order_items)

        self.session.add(order_dbo)
        self.session.commit()
        new_dto = order_dbo_to_dto(order_dbo)
        # print("new dto: ", new_dto)
        return new_dto

    def get_all_order(self) -> OrderDTO:
        base_query = self.session.query(OrderDBO)
        # sort by created_time

        dbos = base_query.order_by(OrderDBO.created_time).all()
        print("==> dbos: ", dbos)
        dtos = [order_dbo_to_dto(dbo) for dbo in dbos]
        return dtos

    def get_order(self, id:UUID) -> OrderDTO:
        order = self.session.query(OrderDBO).get(id)
        if not order:
            raise ObjectNotFound(f"Order id '{id}' not found!")

        new_dto = order_dbo_to_dto(order)
        # print("new dto: ", new_dto)
        return new_dto

    def update_order(self, id: UUID, status: str) -> OrderDTO:

        order = self.session.query(OrderDBO).get(id)
        if not order :
            raise ObjectNotFound(f"Order id '{id}' not found!" )
        order.status = status
        self.session.commit()

        new_dto = order_dbo_to_dto(order)
        # print("new dto: ", new_dto)
        return new_dto

    def get_payment_intent(self, amount: float) -> PaymentIntentDTO:
        intent = stripe.PaymentIntent.create(
            amount=amount, currency="usd"
        )
        payment_intent_dto = PaymentIntentDTO(client_secret=intent["client_secret"])
        return payment_intent_dto