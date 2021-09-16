# resources/order_resource.py
from flask import request, Response, abort, jsonify
from utils.exceptions import ObjectAlreadyExists
from uuid import UUID
from schemas.order_schema import OrderSchema
from dto_models.app_order_dto import OrderDTO
from services.order_service import OrderService
import logging

logger = logging.getLogger(__name__)

class OrderResource:
    # create(post), get_by_id, get_all, update, delete
    @staticmethod
    def post() -> Response:
        try:
            json = request.get_json(force=True)  # get from body
            print(json)
            print("Hello form resource!")
            schema = OrderSchema()
            validated_json = schema.load(json)  # Validated data from frontend
            print("\nvalidated_json:", validated_json)
            dto = OrderDTO(**validated_json)  # transform to DTO OBJECT
            print("\n DTO: ", dto)
            returned_dto = OrderService().create(dto)

        except ValueError as e:
            abort(400, {'message': str(e)})
            logger.debug("Promotion Type Resource post 400 {}".format(e))
        except ObjectAlreadyExists as e:
            abort(400, {'message': str(e)})
            logger.debug("Promotion Type Resource  post 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("Promotion Type Resource  post 500 {}".format(e))

        # Dumps to UI format (json)
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")
        # return "hello-->"

    @staticmethod
    def get_all_order() ->Response:
        try:
            returned_dto = OrderService().get_all_order()
        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("Order resource: get all order get 500 {}".format(e))

            # Dumps to UI format (json)
        schema = OrderSchema(many=True)
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def get_order(order_id: UUID) ->Response:
        try:
            returned_dto = OrderService().get_order(order_id)
        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("Order resource: get order get 500 {}".format(e))

            # Dumps to UI format (json)
        schema = OrderSchema()
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")


    @staticmethod
    def update_order(order_id: UUID) -> Response:
        try:
            json = request.get_json(force=True)  # get from body
            # schema = OrderSchema()

            # validated_json = schema.load(json)  # Validated data from frontend
            #  dto = OrderDTO(**validated_json)  # transform to DTO OBJECT
            returned_dto = OrderService().update_order(order_id, json["status"])

        except ValueError as e:
            abort(400, {'message': str(e)})
            logger.debug("Promotion Type Resource post 400 {}".format(e))
        except ObjectAlreadyExists as e:
            abort(400, {'message': str(e)})
            logger.debug("Promotion Type Resource  post 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("Promotion Type Resource  post 500 {}".format(e))

        schema = OrderSchema()
        # Dumps to UI format (json)
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")
