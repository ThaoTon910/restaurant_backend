from schemas.merchant import MerchantSchema
from dto_models.merchant import MerchantDTO
from dto_models.hour import HourDTO
from services.merchant import MerchantService
from flask import request, Response, abort
from utils.exceptions import ObjectAlreadyExists, ObjectNotFound, InvalidOperation
from uuid import UUID
import logging

logger = logging.getLogger(__name__)


class MerchantResource:
    # create(post), get_by_id, get_all, update, delete
    @staticmethod
    def post() -> Response:
        try:
            json = request.get_json(force=True)  # get from body
            schema = MerchantSchema()
            validated_json = schema.load(json)  # Validated data from frontend
            validated_json['hours'] = [HourDTO(**hour) for hour in validated_json['hours']]
            dto = MerchantDTO(**validated_json)  # transform to DTO OBJECT

            returned_dto = MerchantService().create(dto)

        except ValueError as e:
            abort(400, {'message': str(e)})
            logger.debug("MerchantResource post 400 {}".format(e))
        except ObjectAlreadyExists as e:
            abort(400, {'message': str(e)})
            logger.debug("MerchantResource post 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("MerchantResource post 500 {}".format(e))

        # Dumps to UI format (json)
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def get_merchant() -> Response:
        try:
            returned_dto = MerchantService().get_merchant()
        except ValueError as e:
            abort(400, {'message': str(e)})
        except ObjectNotFound as e:
            abort(400, {'message': str(e)})
            logger.debug("MerchantResource post 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("MerchantResource get 500 {}".format(e))

            # Dumps to UI format (json)
        schema = MerchantSchema()
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def update() -> Response:
        try:
            json = request.get_json(force=True)  # get from body
            schema = MerchantSchema()
            validated_json = schema.load(json)  # Validated data from frontend
            validated_json['hours'] = [HourDTO(**hour) for hour in validated_json['hours']]
            dto = MerchantDTO(**validated_json)  # transform to DTO OBJECT
            # dto.id = id
            returned_dto = MerchantService().update(dto)

        except ValueError as e:
            abort(400, {'message': str(e)})
            logger.debug("MerchantResource post 400 {}".format(e))
        except ObjectNotFound as e:
            abort(400, {'message': str(e)})
            logger.debug("MerchantResource post 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("MerchantResource post 500 {}".format(e))

        # Dumps to UI format (json)
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def delete() -> Response:
        try:
            returned_dto = MerchantService().delete()
        except ValueError as e:
            abort(400, {'message': str(e)})
        except ObjectNotFound as e:
            abort(400, {'message': str(e)})
            logger.debug("MerchantResource post 400 {}".format(e))
        except InvalidOperation as e:
            abort(400, {'message': str(e)})
            logger.debug("MerchantResource delete 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("MerchantResource get 500 {}".format(e))

        # Dumps to UI format (json)
        schema = MerchantSchema()
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")
