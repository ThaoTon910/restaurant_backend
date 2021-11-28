from datetime import datetime
from marshmallow import fields
from schemas import BaseSchema
from dto_models.merchant import MerchantDTO
from schemas.hour import HourSchema
from typing import List
class MerchantSchema(BaseSchema):
     # Resource
     name = fields.String(required=True)
     phone = fields.String(required=True)
     address = fields.String(required=True)
     hours = fields.List(fields.Nested(HourSchema), required=True)

     # Dump to UI
     id = fields.UUID(dump_only=True)
     createdTime = fields.DateTime(dump_only=True, format='iso8601', attribute="created_time")
     updatedTime = fields.DateTime(dump_only=True, format='iso8601', attribute="updated_time")


#Test
if __name__ == '__main__':
     import uuid
     merchant_json = {
        'name': "My Store",
        'phone': "my phone",
        'address': "my address",
        'hours': [
            dict(day='Monday', start='09:00:00', end='22:00:00', off=False),
            dict(day='Tuesday', start='09:00:00', end='22:00:00', off=False),
            dict(day='Wednesday', start='09:00:00', end='22:00:00', off=False),
            dict(day='Thursday', start='09:00:00', end='22:00:00', off=False),
            dict(day='Friday', start='09:00:00', end='22:00:00', off=False),
            dict(day='Saturday', start='09:00:00', end='22:00:00', off=False),
            dict(day='Sunday', start='09:00:00', end='22:00:00', off=False),
        ]
    }
     merchant_schemas = MerchantSchema()
     schema_hour = HourSchema(many=True)

     print(merchant_schemas.load(merchant_json))

     #Test on http://192.168.1.43:8080/v0/ui/#/default/app.create_merchant
     # {
     #     "address": "my address",
     #     "phone": "my phone",
     #     "name": "My Store",
     #     "hours": [
     #         {
     #             "day": "Monday",
     #             "end": "22:00:00",
     #             "start": "09:00:00",
     #             "off": false
     #         },
     #         {
     #             "day": "Tuesday",
     #             "end": "22:00:00",
     #             "start": "09:00:00",
     #             "off": false
     #         },
     #         {
     #             "day": "Wednesday",
     #             "end": "22:00:00",
     #             "start": "09:00:00",
     #             "off": false
     #         },
     #         {
     #             "day": "Thursday",
     #             "end": "22:00:00",
     #             "start": "09:00:00",
     #             "off": false
     #         },
     #         {
     #             "day": "Friday",
     #             "end": "22:00:00",
     #             "start": "09:00:00",
     #             "off": false
     #         },
     #         {
     #             "day": "Saturday",
     #             "end": "22:00:00",
     #             "start": "09:00:00",
     #             "off": false
     #         },
     #         {
     #             "day": "Sunday",
     #             "end": "22:00:00",
     #             "start": "09:00:00",
     #             "off": false
     #         }
     #     ]
     # }