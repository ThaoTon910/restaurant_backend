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
from dbo_models.promotion import PromotionDBO
from dto_models.promocode import PromoCodeDTO
from dbo_models.extra_percentage_all import ExtraPercentageAllDBO

from services.extra_percentage_all import ExtraPercentageAllService


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
        percent_off = 0.0
        print(f"\npromo_code: {dto.promo_code} \n")

        if dto.promo_code != "":
            if self._is_code_valid(dto.promo_code):
                active_pc = self.session.query(PromotionDBO).filter_by(promo_code=dto.promo_code, is_active=True).first()
                promo_type = str(active_pc.promotion_type.promotion_type)
                if promo_type == "extra_percentage_all":
                    percent_off = self.get_percent_off()
                    print(f"\npercent_off: {percent_off} \n")
                else:
                    return dto
            else:
                return dto

        order_dbo = OrderDBO(dto)
        customer_dbo = None
        if "id" in dto.customer:
            customer_dbo = self.session.query(CustomerDBO).get(dto.customer["id"])
            if customer_dbo == None:
                customer_dbo = CustomerDBO(first_name=dto.customer["first_name"],
                                        last_name=dto.customer["last_name"],
                                        email=dto.customer["email"],
                                        phone_number=dto.customer["phone_number"])
                customer_dbo.id = dto.customer["id"]
        else:
            customer_dbo = CustomerDBO(first_name=dto.customer["first_name"],
                                        last_name=dto.customer["last_name"],
                                        email=dto.customer["email"],
                                        phone_number=dto.customer["phone_number"])
        
        order_dbo.customer = customer_dbo

        # print(dto.delivery)
        delivery = DeliveryDBO(delivery_type=dto.delivery["info"]["delivery_type"],
                               fee=dto.delivery["delivery_fee"],
                               time=dto.delivery["info"]["time"],
                               merchant_id=dto.delivery["info"]["merchant_id"])
        delivery.order = order_dbo
        # print(delivery)

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


        print(f"\nsubtotal: {subtotal} \n")

        order_dbo.discount = subtotal * percent_off
        subtotal = (subtotal - order_dbo.discount)
        subtotal += subtotal*order_dbo.tip_multiplier + subtotal*order_dbo.tax_multiplier
        print(f"\nsubtotal AFTER: {subtotal} \n")


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

    def _is_code_valid(self, pc: str) -> bool:
        active_pc_list = self.session.query(PromotionDBO).filter_by(promo_code=pc).all()
        # this look for an active promo code. A promo code can be use in different times.
        # such as there are many code "GET20OFF" but the begin and the end time is different!
        # make sure we look for all the code that is in ACTIVE in the table
        if active_pc_list is not None:
            for p_code in active_pc_list:
                if p_code.is_active:
                    return True
        return False

    @staticmethod
    def get_extra_percentage_all(order: PromoCodeDTO) -> PromoCodeDTO:
        extra_pc = ExtraPercentageAllService().get_percent_off()
        total_discount = round(order.sub_total * extra_pc, 2)
        order.total_discount = total_discount
        order.sub_total = order.sub_total - total_discount
        return order

    def get_percent_off(self) -> float:
        dbo = self.session.query(ExtraPercentageAllDBO).first()
        if not dbo:
            raise ObjectNotFound("Promotion type fetch failed")
        percent_off = dbo.percent_off
        # return the list in dto format
        return percent_off

    def promotion_code(self, dto: OrderDTO) -> OrderDTO:
        print(f"\nIn serviece PC: {dto} \n")
        order = dto
        promo_code = order.promo_code
        # check if the promo code is valid and in ACTIVE
        if self._is_code_valid(promo_code):
            print(f"\nIn serviece: code active \n")

            active_pc = self.session.query(PromotionDBO).filter_by(promo_code=promo_code, is_active=True).first()
            if not active_pc:
                return 0.0
            promo_type = str(active_pc.promotion_type.promotion_type)
            if promo_type == "extra_percentage_all":
                percent_off = self.get_percent_off()
                print(f"\npercent_off: {percent_off} \n")
                return percent_off
        else:
            return 0.0