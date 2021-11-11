# services/order_service.py
import logging
import os
import stripe
from dotenv import load_dotenv
from uuid import UUID
from services._base import BaseService
from utils.exceptions import *
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
from dbo_models.payment import PaymentDBO

logger = logging.getLogger(__name__)
load_dotenv()
stripe.api_key = os.getenv('STRIPE_SK')

# working with database, and logic
class OrderService(BaseService):
    def __init__(self) -> None:
        super().__init__()

    # def _is_id_exist(self, promotion_id: UUID) -> bool:
    #     return self.session.query(PromotionDBO).filter_by(id=promotion_id).first()

    # create new promotion in table "promotion", get data from resource
    def create(self, dto: OrderDTO) -> OrderDTO:
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
        delivery.order = order_dbo
        order_dbo.discount=0.0

        subtotal = 0.0
        for item in dto.items:
            item_dbo = self.session.query(MenuItemDBO).get(item["menu_item_id"])
            price = item_dbo.price
            order_item_dbo = OrderItemDBO(order=order_dbo, menu_item=item_dbo, quantity=item["quantity"],
                                          special_instruction=item["special_instruction"])
            if "add_ons" in  item:
                for addon in item["add_ons"]:
                    add_on_dbo = self.session.query(AddonDBO).get(addon)
                    price += add_on_dbo.price
                    order_item_dbo.add_ons.append(add_on_dbo)
            subtotal += price
            order_item_dbo.price = price

        payment_intent = self.get_payment_intent(amount=round(subtotal*100), email=customer_dbo.email)
        payment_dbo = PaymentDBO(payment_intent_id = payment_intent.id, client_secret=payment_intent.client_secret)
        payment_dbo.order = order_dbo
        self.session.add(order_dbo)
        self.session.commit()

        new_dto = order_dbo_to_dto(order_dbo)
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

    def get_payment_intent(self, amount: float, email: str):
        return stripe.PaymentIntent.create(
            amount=amount, currency="usd", receipt_email=email
        )


    def process_payment(self, payment_intent_id: str, receipt_url: str):
        payment = self.session.query(PaymentDBO).filter_by(payment_intent_id=payment_intent_id).first()
        if not payment:
            raise ObjectNotFound(f"payment_intent_id: '{payment_intent_id}' not found!")\

        payment.receipt_url = receipt_url
        payment.order.status = "pending"
        self.session.commit()
        order_dto = order_dbo_to_dto(payment.order)
        return order_dto
