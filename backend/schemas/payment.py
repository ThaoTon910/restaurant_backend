# schema/payment.py

from marshmallow import fields
from schemas import BaseSchema


class PaymentSchema(BaseSchema):
    #Resource
    paymentIntentId = fields.String(dump_only=True, attribute='payment_intent_id')
    clientSecret = fields.String(dump_only=True, attribute='client_secret')
    receiptURL = fields.String(dump_only=True, attribute='receipt_url')
    refunded = fields.Boolean(dump_only=True)
