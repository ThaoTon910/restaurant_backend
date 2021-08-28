# services/promocode.py
from dbo_models.promotion import PromotionDBO
from dto_models.promocode import PromoCodeDTO
from services._base import BaseService
from services.promotion import PromotionService
from services.extra_percentage_all import ExtraPercentageAllService

from utils.exceptions import *
from uuid import UUID
from typing import List
import logging

logger = logging.getLogger(__name__)


class PromoCodeService(BaseService):
    def __init__(self) -> None:
        super().__init__()

    def _is_valid(self, pc: str) -> bool:
        active_pc_list = self.session.query(PromotionDBO).filter_by(promo_code=pc).all()
        # this look for an active promo code. A promo code can be use in different times.
        # such as there are many code "GET20OFF" but the begin and the end time is different!
        # make sure we look for all the code that is in ACTIVE in the table
        if active_pc_list is not None:
            for p_code in active_pc_list:
                if p_code.is_active:
                    return True
        return False

    def get_extra_percentage_all(self, order: PromoCodeDTO) -> PromoCodeDTO:
        extra_pc = ExtraPercentageAllService().get_percent_off()
        total_discount = round(order.sub_total * extra_pc, 2)
        order.total_discount = total_discount
        order.sub_total = order.sub_total - total_discount
        return order

    def get_promotion(self, dto: PromoCodeDTO) -> PromoCodeDTO:
        order = dto
        promo_code = order.promo_code
        # check if the promo code is valid and in ACTIVE
        if self._is_valid(promo_code):
            active_pc = self.session.query(PromotionDBO).filter_by(promo_code=promo_code, is_active=True).first()
            promo_type = str(active_pc.promotion_type.promotion_type)
            if promo_type == "extra_percentage_all":
                promo_order = self.get_extra_percentage_all(order)
                return promo_order
            else:
                print(f"NO THING CATCH \n")

        else:


            return dto

        """
        If the promotion code is NOT valid or is_ACTIVE = false, return NONE
        If the promotion code is valid:
               From promotion type we can check the discount / extra off for each item in the order    
               In this example, the promotion type = extra_percentage_all, we collect the percentage off in 
               extra_percentage_all table
        """
