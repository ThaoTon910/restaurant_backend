# resources/order.py
from schemas.promotion_type import PromotionTypeSchema
from dto_models.promotion_type import PromotionTypeDTO
from services.promotion_type import PromotionTypeService
from flask import request, Response, abort, jsonify
from utils.exceptions import ObjectAlreadyExists
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

class OrderResource:
    # create(post), get_by_id, get_all, update, delete
    @staticmethod
    def post() -> Response:
        try:
            json = request.get_json(force=True)  # get from body
            schema = PromotionTypeSchema()
            validated_json = schema.load(json)  # Validated data from frontend
            dto = PromotionTypeDTO(**validated_json)  # transform to DTO OBJECT
            returned_dto = PromotionTypeService().create(dto)

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
