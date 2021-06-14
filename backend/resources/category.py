from flask import request, Response, abort
from schemas.category import CategorySchema
from dto_models.category import Category as CategoryDTO
from functools import partial

import logging
logger = logging.getLogger(__name__)

class CategoryResource:

    @staticmethod
    def post() -> Response:
        try:
            json = request.get_json(force=True)
            schema = CategorySchema()
            validated_json = schema.load(json) #Validated data from frontend
            dto = CategoryDTO(**validated_json) #transform to DTO OBJECT

            # data = CategoryService().create(dto)
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
        response_data = schema.dumps(dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")