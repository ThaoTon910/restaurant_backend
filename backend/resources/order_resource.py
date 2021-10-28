# resources/order_resource.py
import stripe
import json
from flask import request, Response, abort, jsonify
from utils.exceptions import ObjectAlreadyExists
from uuid import UUID
from schemas.order_schema import OrderSchema
from schemas.client_secret import ClientSecret
from dto_models.app_order_dto import OrderDTO
from services.order_service import OrderService
from schemas.payment_intent import PaymentIntentSchema
import logging

logger = logging.getLogger(__name__)

stripe.api_key = "sk_test_51Jno9iJtWODUig1GpEc6isyYnuA51IPjJ1c3fIvEWbOVA09y8LUNSmU3uRifuKiKq4augXBylY5q9VGoelqy13Jn00sJCKAEyx"


class OrderResource:
    @staticmethod
    # send payment intent to stripe
    def create_payment() -> Response:
        data = json.loads(request.data)
        try:
            if "amount" in data:
                try:
                    intent = stripe.PaymentIntent.create(
                        amount=data["amount"], currency="usd"
                    )
                    return jsonify({"client_secret": intent["client_secret"]}), 200
                    print(response_data)
                except ValueError as e:
                    return jsonify(error=str(e)), 400
            else:
                return jsonify(error="No amount to pay in request"), 400
        except Exception as e:
            return jsonify(error=str(e)), 500


    # create(post), get_by_id, get_all, update, delete
    @staticmethod
    def post() -> Response:
        try:
            json = request.get_json(force=True)  # get from body
            print(json)
            print("Hello form resource!")
            schema = OrderSchema()
            validated_json = schema.load(json)  # Validated data from frontend
            print("\nvalidated_json:", validated_json)
            dto = OrderDTO(**validated_json)  # transform to DTO OBJECT
            print("\n DTO: ", dto)
            returned_dto = OrderService().create(dto)

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
        # return "hello-->"

    @staticmethod
    def get_all_order() -> Response:
        try:
            returned_dto = OrderService().get_all_order()
        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("Order resource: get all order get 500 {}".format(e))

            # Dumps to UI format (json)
        schema = OrderSchema(many=True)
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def get_order(order_id: UUID) -> Response:
        try:
            returned_dto = OrderService().get_order(order_id)
        except ValueError as e:
            abort(400, {'message': str(e)})
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("Order resource: get order get 500 {}".format(e))

            # Dumps to UI format (json)
        schema = OrderSchema()
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def update_order(order_id: UUID) -> Response:
        try:
            json = request.get_json(force=True)  # get from body
            # schema = OrderSchema()

            # validated_json = schema.load(json)  # Validated data from frontend
            #  dto = OrderDTO(**validated_json)  # transform to DTO OBJECT
            returned_dto = OrderService().update_order(order_id, json["status"])

        except ValueError as e:
            abort(400, {'message': str(e)})
            logger.debug("Promotion Type Resource post 400 {}".format(e))
        except ObjectAlreadyExists as e:
            abort(400, {'message': str(e)})
            logger.debug("Promotion Type Resource  post 400 {}".format(e))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("Promotion Type Resource  post 500 {}".format(e))

        schema = OrderSchema()
        # Dumps to UI format (json)
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")

    @staticmethod
    def create_payment_intent() -> Response:
        try:
            json = request.get_json(force=True)  # get from body

            if not json.get("amount"):
                abort(400, {'message': 'invalid amount'})
            returned_dto = OrderService().get_payment_intent(amount=json.get("amount"))
        except Exception as e:
            abort(500, {'message': str(e)})
            logger.debug("Payment Indent Type Resource  post 500 {}".format(e))

        schema = PaymentIntentSchema()
        # Dumps to UI format (json)
        response_data = schema.dumps(returned_dto)

        return Response(response_data, status=200, headers={}, mimetype="application/json")
