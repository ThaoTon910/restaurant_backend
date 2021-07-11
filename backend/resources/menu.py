from uuid import UUID
from utils.exceptions import *
from flask import request, Response, abort
from schemas.menu import MenuSchema
from services.menu import MenuService
from dto_models.menu_item import MenuItemDTO
from services.menu_item import MenuItemService
from utils.exceptions import ObjectAlreadyExists
import logging
logger = logging.getLogger(__name__)

class MenuResource:

    @staticmethod
    def get_menu() -> Response:
        try:
            returned_dto = MenuService().get_menu()
        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("MenuItemResource get 500 {}".format(e))

            # Dumps to UI format (json)
        schema = MenuSchema()
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")