from uuid import UUID
from utils.exceptions import *
from flask import request, Response, abort
from schemas.menu_item import MenuItemSchema
from dto_models.menu_item import MenuItemDTO
from services.menu_item import MenuItemService
from utils.exceptions import ObjectAlreadyExists, ObjectNotFound
import logging
logger = logging.getLogger(__name__)

class MenuItemResource:
    @staticmethod
    def post() -> Response:
        schema = MenuItemSchema()
        try:
            json = request.get_json(force=True) #get from body
            validated_json = schema.load(json) #Validated data from frontend
            dto = MenuItemDTO(**validated_json) #transform to DTO OBJECT
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
    def get_by_id(id: UUID) -> Response:
        try:
            returned_dto = MenuItemService().get_by_id(id)
        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("MenuItemResource get 500 {}".format(e))

            # Dumps to UI format (json)
        schema = MenuItemSchema()
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

    #Extra--but using the backref database
    @staticmethod
    def get_menu_items_from_category(id: UUID) -> Response:
        try:
            returned_dtos = MenuItemService().get_menu_items_from_category(id)
        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("Addon Resource get 500 {}".format(e))

            # Dumps to UI format (json)
        schema = MenuItemSchema(many=True)
        response_data = schema.dumps(returned_dtos)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def update(id: UUID) -> Response:
        try:
            json = request.get_json(force=True)  # get from body
            schema = MenuItemSchema()
            validated_json = schema.load(json)  # Validated data from frontend
            dto = MenuItemDTO(**validated_json)  # transform to DTO OBJECT
            dto.id = id
            returned_dto = MenuItemService().update(dto)

        except ValueError as e:
            abort(400, {'message': str(e)})
            logger.debug("MenuItemResource post 400 {}".format(e))
        except ObjectNotFound as e:
            abort(400, {'message': str(e)})
            logger.debug("MenuItemResource post 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("MenuItemResource post 500 {}".format(e))

        # Dumps to UI format (json)
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def delete(id: UUID) -> Response:
        try:
            returned_dto = MenuItemService().delete(id)
        except ValueError as e:
            abort(400, {'message': str(e)})
        except ObjectNotFound as e:
            abort(400, {'message': str(e)})
            logger.debug("MenuItemResource post 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("MenuItemResource get 500 {}".format(e))

            # Dumps to UI format (json)
        schema = MenuItemSchema()
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")