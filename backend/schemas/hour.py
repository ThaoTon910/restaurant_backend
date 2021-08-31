from schemas import BaseSchema
from marshmallow import fields, post_load
from marshmallow.validate import OneOf
# from dto_models.hour import Hour as HourDTO
import datetime
class MyTimeField(fields.Time):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, datetime.time):
            return value
        return super()._deserialize(value, attr, data, **kwargs)

class HourSchema(BaseSchema):
    start = MyTimeField(required=True, format='iso8601')
    end = MyTimeField(required=True, format='iso8601', type=str)
    day = fields.String(required=True, type=str, validate=OneOf(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']))
    off = fields.Boolean(required=False, type=bool, default=False)

    # @post_load
    # def make_object(self, data, **kwargs):
    #     return HourDTO(**data)
