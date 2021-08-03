
from schemas.addon import AddonSchema
from dto_models.addon import AddonDTO
from services.addon import AddonService
from flask import request, Response, abort
from utils.exceptions import ObjectAlreadyExists, ObjectNotFound
from uuid import UUID
import logging
logger = logging.getLogger(__name__)

class AddonResource:
    @staticmethod
    # create(post), get_all, get_by_id
    def post() -> Response:
        schema = AddonSchema()
        try:
            json = request.get_json(force=True)#get json form body
            validated_schema =  schema.load(json) #Validated data from frontend
            dto = AddonDTO(**validated_schema) #transform to DTO OBJECT
            returned_dto = AddonService().create(dto)
        except ValueError as e:
            abort(400, {'message': str(e)})
            logger.debug("AddonResource post 400 {}".format(e))
        except ObjectAlreadyExists as e:
            abort(400, {'message': str(e)})
            logger.debug("AddonResource post 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("AddonResource post 500 {}".format(e))


        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def get_all_addons() -> Response:
        try:
            returned_dto = AddonService().get_all_addons()
        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("AddonResource get 500 {}".format(e))

            # Dumps to UI format (json)
        schema = AddonSchema(many=True)
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def get_addons_from_group(id: UUID) -> Response:
        try:
            returned_dtos = AddonService().get_addons_from_group(id)
        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("Addon Resource get 500 {}".format(e))

            # Dumps to UI format (json)
        schema = AddonSchema(many=True)
        response_data = schema.dumps(returned_dtos)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def get_by_id(id: UUID) -> Response:
        try:
            returned_dto = AddonService().get_by_id(id)
        except ValueError as e:
            abort(400, {'message': str(e)})
        except ObjectNotFound as e:
            abort(400, {'message': str(e)})
            logger.debug("AddonResource post 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("AddonResource get 500 {}".format(e))

            # Dumps to UI format (json)
        schema = AddonSchema()
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def update(id: UUID) -> Response:
        try:
            json = request.get_json(force=True)  # get from body
            schema = AddonSchema()
            validated_json = schema.load(json)  # Validated data from frontend
            dto = AddonDTO(**validated_json)  # transform to DTO OBJECT
            dto.id = id
            returned_dto = AddonService().update(dto)

        except ValueError as e:
            abort(400, {'message': str(e)})
            logger.debug("AddonResource post 400 {}".format(e))
        except ObjectNotFound as e:
            abort(400, {'message': str(e)})
            logger.debug("AddonResource post 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("AddonResource post 500 {}".format(e))

        # Dumps to UI format (json)
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def delete(id: UUID) -> Response:
        try:
            returned_dto = AddonService().delete(id)
        except ValueError as e:
            abort(400, {'message': str(e)})
        except ObjectNotFound as e:
            abort(400, {'message': str(e)})
            logger.debug("AddonResource post 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("AddonResource get 500 {}".format(e))

            # Dumps to UI format (json)
        schema = AddonSchema()
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")
