from flask import request, Response, abort
from schemas.category import CategorySchema
from dto_models.category import Category as CategoryDTO
from services.category import CategoryService
from functools import partial
from dbo_models.category import Category as CategoryDBO
from uuid import UUID
import logging
logger = logging.getLogger(__name__)

class CategoryResource:
    @staticmethod
    def get_by_id(id: UUID) -> Response:
        try:
            returned_dto = CategoryService().get_by_id(id)
        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("CategoryResource get 500 {}".format(e))

            # Dumps to UI format (json)
        schema = CategorySchema()
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def post() -> Response:
        try:
            json = request.get_json(force=True) #get from body
            schema = CategorySchema()
            validated_json = schema.load(json) #Validated data from frontend
            dto = CategoryDTO(**validated_json) #transform to DTO OBJECT

            returned_dto = CategoryService().create(dto)
        except ValueError as e:
            abort(400, {'message': str(e)})
            logger.debug("CategoryResource post 400 {}".format(e))
        # except ObjectAlreadyExists as e:
        #     abort(400, {'message': str(e)})
        #     logger.debug("CategoryResource post 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("CategoryResource post 500 {}".format(e))

        #Dumps to UI format (json)
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")