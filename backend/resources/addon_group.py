from schemas.addon_group import AddonGroupSchema
from dto_models.addon_group import AddonGroupDTO
from services.addon_group import AddonGroupService
from flask import Response, request, abort
from uuid import UUID
from utils.exceptions import ObjectAlreadyExists
import logging
logger = logging.getLogger(__name__)
class AddonGroupResource:
    @staticmethod
    def post()-> Response:
        try:
            json = request.get_json(force=True) #get form body
            schemas = AddonGroupSchema()
            validated_schema = schemas.load(json) #Validated data from frontend
            dto = AddonGroupDTO(**validated_schema) #transform to DTO OBJECT

            #After done Services, we call AddonService class to reture DTO
            returned_dto = AddonGroupService().create(dto)

        except ValueError as e:
            abort(400, {'message': str(e)})
        except ObjectAlreadyExists as e:
            abort(400, {'message': str(e)})
            logger.debug("CategoryResource post 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("CategoryResource post 500 {}".format(e))

            #After donne Serivecs, we send back to UI by .dump from returned_dto above
            #Dumps to UI format(json)
        schemas = AddonGroupSchema(many=True)
        response_data = schemas.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def get_all_addon_groups() -> Response:
        try:
            returned_dto = AddonGroupService().get_all_addon_group()
        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("AddonGroup Resource get 500 {}".format(e))

            # Dumps to UI format (json)
        schema = AddonGroupSchema(many=True)
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def get_by_id(id: UUID) -> Response:
        try:
            returned_dto = AddonGroupService().get_by_id(id)
        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("AddonGroupResource get 500 {}".format(e))

            # Dumps to UI format (json)
        schema = AddonGroupSchema()
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def update_addon_group(id: UUID) -> Response:
        pass

    @staticmethod
    def delete_addon_group(id: UUID) -> Response:
        # call the delete method of the category resource, get back the deleted category object

        # serialize the category object into json

        # return the response
        pass


#Test
if __name__== '__main__':
    addon_group_json = {
        'name': 'Group 1',
        'maxQuantity': 3,
        'minQuantity': 0,
    }

    try:
        json = addon_group_json  # get form body
        schemas = AddonGroupSchema()
        validated_schema = schemas.load(json)  # Validated data from frontend
        dto = AddonGroupDTO(**validated_schema)  # transform to DTO OBJECT


    except Exception as e:
        abort(400, {'message': str(e)})
        logger.debug("CategoryResource post 400 {}".format(e))
    # except ObjectAlreadyExists as e:
    #     abort(400, {'message': str(e)})
    #     logger.debug("CategoryResource post 400 {}".format(e))

    except Exception as e:
        abort(500, {'message': str(e)})
        logger.debug("CategoryResource post 500 {}".format(e))

    print(dto)
    #output
    #AddonGroupDTO(name='Group 1', max_quantity=3, min_quantity=0, id=NOTHING, created_time=datetime.datetime(2021, 7, 2, 22, 4, 48, 471132), updated_time=datetime.datetime(2021, 7, 2, 22, 4, 48, 471375))
