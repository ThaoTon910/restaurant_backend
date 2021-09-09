# resources/customer.py
from services.promotion_type import PromotionTypeService
from flask import request, Response, abort, jsonify
from utils.exceptions import ObjectAlreadyExists
from uuid import UUID
from schemas.customer import CustomerSchema
from dto_models.customer import CustomerDTO
from services.customer import CustomerService
import logging

logger = logging.getLogger(__name__)


class CustomerResource:
    # create(post), get_by_id, get_all, update, delete
    @staticmethod
    def post() -> Response:
        try:
            json = request.get_json(force=True)  # get from body
            schema = CustomerSchema()
            validated_json = schema.load(json)  # load data from front end
            customer_dto = CustomerDTO(**validated_json)  # validation data
            returned_customer_dto = CustomerService().create(customer_dto)

        except ValueError as e:
            abort(400, {'message': str(e)})
            logger.debug("Customer Resource post 400 {}".format(e))
        except ObjectAlreadyExists as e:
            abort(400, {'message': str(e)})
            logger.debug("Customer Resource  post 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("Customer Resource  post 500 {}".format(e))

        # Dumps to UI format (json)
        response_data = schema.dumps(returned_customer_dto)
        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def get_all_customer() -> Response:
        try:
            returned_customer_dto = CustomerService().get_all_customer()
        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("Get all customers, error 500 {}".format(e))

            # Dumps to UI format (json)
        schema = CustomerSchema(many=True)
        response_data = schema.dumps(returned_customer_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def get_by_id(customer_id: UUID) -> Response:
        try:
            returned_customer_dto = CustomerService().get_by_id(customer_id)

        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            # abort(500, {'message': str(e)})
            logger.debug("Promotion Type Resource get 500 {}".format(e))
            return jsonify({'promotion_type': 'None',
                            'description': 'None',
                            'message':  str(e)})

            # Dumps to UI format (json)
        schema = CustomerSchema()
        response_data = schema.dumps(returned_customer_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def update_customer(customer_id: UUID) -> Response:
        try:
            json = request.get_json(force=True)  # get from body
            schema = CustomerSchema()
            validated_json = schema.load(json)  # Validated data from frontend
            customer_dto = CustomerDTO(**validated_json)  # transform to DTO OBJECT
            customer_dto.id = customer_dto

            returned_customer_dto = PromotionTypeService().update(customer_dto)

        except ValueError as e:
            abort(400, {'message': str(e)})
            logger.debug("Customer at -Resource- update 400 {}".format(e))
        except ObjectAlreadyExists as e:
            abort(400, {'message': str(e)})
            logger.debug("Customer at -Resource- update  400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("Customer at -Resource- update  500 {}".format(e))

        # Dumps to UI format (json)
        response_data = schema.dumps(returned_customer_dto)
        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def delete_customer(customer_id: UUID) -> Response:
        returned_customer_dto = None
        try:
            returned_customer_dto = PromotionTypeService().delete(customer_id)
        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("Customer at -Resource- delete 500 {}".format(e))

        if returned_customer_dto is None:
            return Response(returned_customer_dto, status=500, headers={}, mimetype="application/json")
        # Dumps to UI format (json)
        schema = CustomerSchema()
        response_data = schema.dumps(returned_customer_dto)
        return Response(response_data, status=200, headers={}, mimetype="application/json")

