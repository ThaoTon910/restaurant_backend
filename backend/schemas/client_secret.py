# schemas/client_secret.py
from marshmallow import fields
from schemas import BaseSchema

class ClientSecret(BaseSchema):
    # Resource
    client_secret = fields.String(required=False,  attribute="client_secret")



