from schemas.menu_item_to_addon_group import MenuItemToAddonGroupSchema
from dto_models.menu_item_to_addon_group import MenuItemToAddonGroupDTO
from services.menu_item_to_addon_group import MenuItemToAddonGroupService
from flask import request, Response, abort
from utils.exceptions import ObjectAlreadyExists
from uuid import UUID
import logging
logger = logging.getLogger(__name__)

class MenuItemToAddonGroupResource:
    # create(post), get_by_id, get_all, update, delete
    @staticmethod
    def post() -> Response:
        try:
            json = request.get_json(force=True)  # get from body
            schema = MenuItemToAddonGroupSchema()
            validated_json = schema.load(json)  # Validated data from frontend
            dto = MenuItemToAddonGroupDTO(**validated_json)  # transform to DTO OBJECT

            returned_dto = MenuItemToAddonGroupService().create(dto)

        except ValueError as e:
            abort(400, {'message': str(e)})
            logger.debug("MenuItemToAddonGroupResource post 400 {}".format(e))
        except ObjectAlreadyExists as e:
            abort(400, {'message': str(e)})
            logger.debug("MenuItemToAddonGroupResource post 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("MenuItemToAddonGroupResource post 500 {}".format(e))

        # Dumps to UI format (json)
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")
    @staticmethod
    def get_all_menu_item_to_addon_groups() -> Response:
        try:
            returned_dto = MenuItemToAddonGroupService().get_all_menu_item_to_addon_groups()
        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("MenuItemToAddonGroupResource get 500 {}".format(e))

            # Dumps to UI format (json)
        schema = MenuItemToAddonGroupSchema(many=True)
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")
    # @staticmethod
    # def get_by_id(id: UUID) -> Response:
    #     try:
    #         returned_dto = MenuItemToAddonGroupService().get_by_id(id)
    #     except ValueError as e:
    #         abort(400, {'message': str(e)})
    #     except Exception as e:
    #         abort(500, {'message': str(e)})
    #         logger.debug("MenuItemToAddonGroupResource get 500 {}".format(e))
    #
    #         # Dumps to UI format (json)
    #     schema = MenuItemToAddonGroupSchema()
    #     response_data = schema.dumps(returned_dto)
    #
    #     return Response(response_data, status=200, headers={}, mimetype="application/json")
    #

