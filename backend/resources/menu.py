from uuid import UUID
from utils.exceptions import *
from flask import request, Response, abort
from schemas.menu_item import MenuItemSchema
from dto_models.menu_item import MenuItemDTO
from services.menu_item import MenuItemService
from utils.exceptions import ObjectAlreadyExists
import logging
logger = logging.getLogger(__name__)

class Menu:
    @staticmethod
    def post() -> Response:
        schema = MenuItemSchema()
        try:
            json = request.get_json(force=True)  # get from body
            validated_json = schema.load(json)  # Validated data from frontend
            dto = MenuItemDTO(**validated_json)  # transform to DTO OBJECT
            returned_dto = MenuItemService().create(dto)
        except ValueError as e:
            abort(400, {'message': str(e)})
            logger.debug("MenuItemResource post 400 {}".format(e))
        except ObjectAlreadyExists as e:
            abort(400, {'message': str(e)})
            logger.debug("MenuItemResource post 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("MenuItemResource post 500 {}".format(e))

        response_data = schema.dumps(returned_dto)
        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def get_all_menu_items() -> Response:
        try:
            returned_dto = MenuItemService().get_all_menu_items()
        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("MenuItemResource get 500 {}".format(e))

            # Dumps to UI format (json)
        schema = MenuItemSchema(many=True)
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")