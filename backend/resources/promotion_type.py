# resources/promotion_type.py
from schemas.promotion_type import PromotionTypeSchema
from dto_models.promotion_type import PromotionTypeDTO
from services.promotion_type import PromotionTypeService
from flask import request, Response, abort, jsonify
from utils.exceptions import ObjectAlreadyExists
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

class PromotionTypeResource:
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

    @staticmethod
    def get_all_promotion_type() -> Response:
        try:
            returned_dto = PromotionTypeService().get_all_promotion_type()
        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("Get all promotion type 500 {}".format(e))

            # Dumps to UI format (json)
        schema = PromotionTypeSchema(many=True)
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def get_by_id(promotion_type_id: UUID) -> Response:
        try:
            returned_dto = PromotionTypeService().get_by_id(promotion_type_id)

        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            #abort(500, {'message': str(e)})
            logger.debug("Promotion Type Resource get 500 {}".format(e))
            return jsonify({'promotion_type': 'None',
                            'description': 'None',
                            'message':  str(e)})

            # Dumps to UI format (json)
        schema = PromotionTypeSchema()
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def update_promotion_type(promotiontype_id: UUID) -> Response:
        try:
            json = request.get_json(force=True)  # get from body
            schema = PromotionTypeSchema()
            validated_json = schema.load(json)  # Validated data from frontend
            dto = PromotionTypeDTO(**validated_json)  # transform to DTO OBJECT
            dto.id = promotiontype_id

            returned_dto = PromotionTypeService().update(dto)

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

    @staticmethod
    def delete_promotion_type(promotion_type_id: UUID) -> Response:
        returned_dto = None
        try:
            returned_dto = PromotionTypeService().delete(promotion_type_id)
        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("Promotion Type Resource get 500 {}".format(e))

        if returned_dto is None:
            return Response(returned_dto, status=500, headers={}, mimetype="application/json")
        # Dumps to UI format (json)
        schema = PromotionTypeSchema()
        response_data = schema.dumps(returned_dto)
        return Response(response_data, status=200, headers={}, mimetype="application/json")

