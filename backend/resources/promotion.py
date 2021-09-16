# resources/promotion.py
from schemas.promotion import PromotionSchema
from dto_models.promotion import PromotionDTO
from services.promotion import PromotionService
from flask import request, Response, abort, jsonify
from utils.exceptions import ObjectAlreadyExists
from uuid import UUID
import logging

logger = logging.getLogger(__name__)

class PromotionResource:
    # create(post), get_by_id, get_all, update, delete
    @staticmethod
    # method post: create new promotion, data get from request body
    def post() -> Response:
        try:
            json = request.get_json(force=True)  # get from body
            schema = PromotionSchema()
            validated_json = schema.load(json)  # Validated data from frontend
            dto = PromotionDTO(**validated_json)  # transform to DTO OBJECT

            returned_dto = PromotionService().create(dto)

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
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    # get the list of all promotions
    def get_all_promotion() -> Response:
        try:
            returned_dto = PromotionService().get_all_promotion()

        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("Get all promotion type 500 {}".format(e))

            # Dumps to UI format (json)
        schema = PromotionSchema(many=True)
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    # get promotion by ID
    def get_by_id(promotion_id: UUID) -> Response:
        try:
            returned_dto = PromotionService().get_by_id(promotion_id)

        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            #abort(500, {'message': str(e)})
            logger.debug("Promotion Type Resource get 500 {}".format(e))
            return jsonify({'promotion_type': 'None',
                            'description': 'None',
                            'message':  str(e)})

            # Dumps to UI format (json)
        schema = PromotionSchema()
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    # delete a promotion
    def delete_promotion(promotion_id: UUID) -> Response:
        returned_dto = None
        try:
            returned_dto = PromotionService().delete(promotion_id)
        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("Promotion Resource get 500 {}".format(e))

        if returned_dto is None:
            return Response(returned_dto, status=500, headers={}, mimetype="application/json")
        # Dumps to UI format (json)
        schema = PromotionSchema()
        response_data = schema.dumps(returned_dto)
        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    # update a promotion
    def update_promotion(promotion_id: UUID) -> Response:
        try:
            json = request.get_json(force=True)
            schema = PromotionSchema()
            validated_json = schema.load(json)

            dto = PromotionDTO(**validated_json)
            dto.id = promotion_id

            returned_dto = PromotionService().update(dto)

        except ValueError as e:
            abort(400, {'message': str(e)})
            logger.debug("Promotion @ Resource post 400 {}".format(e))
        except ObjectAlreadyExists as e:
            abort(400, {'message': str(e)})
            logger.debug("Promotion @ Resource  post 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("Promotion @ Resource  post 500 {}".format(e))

        # Dumps to UI format (json)
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")
