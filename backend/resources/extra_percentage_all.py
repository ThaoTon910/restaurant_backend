# resources/extra_percentage_all.py
from schemas.extra_percentage_all import ExtraPercentageAllSchema
from dto_models.extra_percentage_all import ExtraPercentageAllDTO
from services.extra_percentage_all import ExtraPercentageAllService
from flask import request, Response, abort, jsonify
from utils.exceptions import ObjectAlreadyExists
from uuid import UUID
import logging

logger = logging.getLogger(__name__)


class ExtraPercentageAllResource:
    # create(post), get_all, update. NO delete

    @staticmethod
    def post() -> Response:
        try:
            json = request.get_json(force=True)  # get from body
            schema = ExtraPercentageAllSchema()
            validated_json = schema.load(json)  # Validated data from frontend
            dto = ExtraPercentageAllDTO(**validated_json)  # transform to DTO OBJECT
            returned_dto = ExtraPercentageAllService().create(dto)

        except ValueError as e:
            abort(400, {'message': str(e)})
            logger.debug("Extra Percentage All Resource post 400 {}".format(e))
        except ObjectAlreadyExists as e:
            abort(400, {'message': str(e)})
            logger.debug("Extra Percentage All post 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("Extra Percentage All post 500 {}".format(e))

        # Dumps to UI format (json)
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    # get the list of all promotions
    def get_all() -> Response:
        try:
            returned_dto = ExtraPercentageAllService().get_all()
        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("Extra Percentage All 500 {}".format(e))

            # Dumps to UI format (json)
        schema = ExtraPercentageAllSchema(many=True)
        response_data = schema.dumps(returned_dto)
        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    # get promotion by ID
    def get_by_id(id: UUID) -> Response:
        try:
            returned_dto = ExtraPercentageAllService().get_by_id(id)
        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            # abort(500, {'message': str(e)})
            logger.debug("Extra Percentage All get by id 500 {}".format(e))
            return jsonify({'promotion_type': 'None',
                            'percentage_off': '0.0',
                            'message': str(e)})

        # Dumps to UI format (json)
        schema = ExtraPercentageAllSchema()
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    # delete a promotion
    def delete_extra_percentage_all(id: UUID) -> Response:
        returned_dto = None
        try:
            returned_dto = ExtraPercentageAllService().delete(id)
        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("Extra Percentage All get 500 {}".format(e))

        if returned_dto is None:
            return Response(returned_dto, status=500, headers={}, mimetype="application/json")
        # Dumps to UI format (json)
        schema = ExtraPercentageAllSchema()
        response_data = schema.dumps(returned_dto)
        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    # update a promotion
    def update_extra_percentage_all(id: UUID) -> Response:
        try:
            json = request.get_json(force=True)
            schema = ExtraPercentageAllSchema()
            validated_json = schema.load(json)
            dto = ExtraPercentageAllDTO(**validated_json)
            if 0.0 <= dto.percent_off <= 1.0:
                print(f"update_extra_percentage_all {dto.percent_off}")
                dto.id = id
                returned_dto = ExtraPercentageAllService().update(dto)
            else:
                return Response(None, status=200, headers={"message": "invalid input for percent off value"},
                                mimetype="application/json")

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
