from schemas.category import CategorySchema
from dto_models.category import CategoryDTO
from services.category import CategoryService
from flask import request, Response, abort
from utils.exceptions import ObjectAlreadyExists, ObjectNotFound, InvalidOperation
from uuid import UUID
import logging

logger = logging.getLogger(__name__)


class CategoryResource:
    # create(post), get_by_id, get_all, update, delete
    @staticmethod
    def post() -> Response:
        try:
            json = request.get_json(force=True)  # get from body
            schema = CategorySchema()
            validated_json = schema.load(json)  # get data  from frontend to validate
            dto = CategoryDTO(**validated_json)  # transform to DTO OBJECT
            returned_dto = CategoryService().create(dto)

        except ValueError as e:
            abort(400, {'message': str(e)})
            logger.debug("CategoryResource post 400 {}".format(e))
        except ObjectAlreadyExists as e:
            abort(400, {'message': str(e)})
            logger.debug("CategoryResource post 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("CategoryResource post 500 {}".format(e))

        # Dumps to UI format (json)
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def get_all_categories() -> Response:
        try:
            returned_dto = CategoryService().get_all_categories()
        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("CategoryResource get 500 {}".format(e))

            # Dumps to UI format (json)
        schema = CategorySchema(many=True)
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def get_by_id(id: UUID) -> Response:
        try:
            returned_dto = CategoryService().get_by_id(id)
        except ValueError as e:
            abort(400, {'message': str(e)})
        except ObjectNotFound as e:
            abort(400, {'message': str(e)})
            logger.debug("CategoryResource post 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("CategoryResource get 500 {}".format(e))

            # Dumps to UI format (json)
        schema = CategorySchema()
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def update(id: UUID) -> Response:
        try:
            json = request.get_json(force=True)  # get from body
            schema = CategorySchema()
            validated_json = schema.load(json)  # Validated data from frontend
            dto = CategoryDTO(**validated_json)  # transform to DTO OBJECT
            dto.id = id
            returned_dto = CategoryService().update(dto)

        except ValueError as e:
            abort(400, {'message': str(e)})
            logger.debug("CategoryResource post 400 {}".format(e))
        except ObjectNotFound as e:
            abort(400, {'message': str(e)})
            logger.debug("CategoryResource post 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("CategoryResource post 500 {}".format(e))

        # Dumps to UI format (json)
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def delete(id: UUID) -> Response:
        try:
            returned_dto = CategoryService().delete(id)
        except ValueError as e:
            abort(400, {'message': str(e)})
        except ObjectNotFound as e:
            abort(400, {'message': str(e)})
            logger.debug("CategoryResource delete 400 {}".format(e))
        except InvalidOperation as e:
            abort(400, {'message': str(e)})
            logger.debug("CategoryResource delete 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("MenuItemResource get 500 {}".format(e))

        # Dumps to UI format (json)
        schema = CategorySchema()
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")