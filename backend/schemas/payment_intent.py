from datetime import datetime
from marshmallow import fields
from schemas import BaseSchema


class PaymentIntentSchema(BaseSchema):
    #Resource
    clientSecret = fields.String(dump_only=True, attribute='client_secret')
