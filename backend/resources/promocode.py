# resources/PromoCode.py
from schemas.promocode import PromoCodeSchema
from schemas.promotion import PromotionSchema
from dto_models.promocode import PromoCodeDTO
from services.promocode import PromoCodeService
from flask import request, Response, abort, jsonify
from utils.exceptions import ObjectAlreadyExists
from dto_models.app_order_dto import OrderDTO
from schemas.order_schema import  OrderSchema
from services.order_service import OrderService
from uuid import UUID
import logging

logger = logging.getLogger(__name__)


class PromoCodeResource:
    used_promo_code = {"promo_code": []}

    def is_used(self, order_id) -> bool:
        for pc in self.used_promo_code.keys():
            if  order_id in self.used_promo_code[pc]:
                return True
        return False

    @staticmethod
    def get_percent_off() -> Response:
        try:
            json = request.get_json(force=True)  # get from body
            print(json)
            print("Hello form resource!")
            schema = OrderSchema()
            validated_json = schema.load(json)  # Validated data from frontend
            print("\nvalidated_json:", validated_json)
            dto = OrderDTO(**validated_json)  # transform to DTO OBJECT
            print("\n DTO: ", dto)
            percent_off = OrderService().promotion_code(dto)

        except ValueError as e:
            abort(400, {'message': str(e)})
            logger.debug("Promotion Type Resource post 400 {}".format(e))
        except ObjectAlreadyExists as e:
            abort(400, {'message': str(e)})
            logger.debug("Promotion Type Resource  post 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("Promotion Type Resource  post 500 {}".format(e))

        return jsonify(percent_off=percent_off)


    @staticmethod
    def post() -> Response:
        response_data = {}
        try:
            json = request.get_json(force=True)  # get from body
            print(json)

            schema = PromoCodeSchema()
            validated_promo = schema.load(json)  # Validated data from frontend
            dto = PromoCodeDTO(**validated_promo)
            if dto.promo_code is not None:
                returned_dto = PromoCodeService().get_promotion(dto)

        except ValueError as e:
            abort(400, {'message': str(e)})
            logger.debug("Promotion @ Resource post 400 {}".format(e))
        except ObjectAlreadyExists as e:
            abort(400, {'message': str(e)})
            logger.debug("Promotion @ Resource  post 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("Promotion  @ Resource  post 500 {}".format(e))

        # Dumps to UI format (json)
        temp_schema = PromoCodeSchema()
        response_data = temp_schema.dumps(returned_dto)
        return Response(response_data, status=200, headers={}, mimetype="application/json")

# if __name__== '__main__':
# promo_code_data = {
#         "is_valid": False,
#         "promo_code": "GET20OFF",
#         "order_item": {"item 1":
#                         {
#                                 "menu_item": "90dcfe02-5514-4d80-9b76-8063b569271c",
#                                 "quantity": 2,
#                                 "item_price": 20.50,
#                                 "discount": 0.0
#
#                         },
#                         "item 2": {
#                             "menu_item": "90dcfe02-5514-4d80-9b76-8063b569271c",
#                             "quantity": 2,
#                             "item_price": 20.50,
#                             "discount": 0.0
#
#                         }
#                     },
#         "sub_total":  41.0,
#         "shipping_fee":  0.0,
#         "shipping_discount": 0.0
#         }
# try:
#     json = promo_code_data
#     schema = PromoCodeSchema()
#     validated_promo = schema.load(json)  # Validated data from frontend
#     validated_promo["is_valid"] = False
#     dto = PromoCodeDTO(**validated_promo)
#
#     # returned_dto = PromoCodeService.get_promotion( None, dto=dto ) # nice !
#     returned_dto = PromoCodeService().get_promotion(dto)
#
# except ValueError as e:
#    abort(400, {'message': str(e)})
