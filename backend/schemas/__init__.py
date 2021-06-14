from marshmallow import Schema, EXCLUDE

class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    # SKIP_TYPES = {type(None)} # set([type(None)])
    #
    # @post_dump
    # def remove_skip_types(self, data: Dict, many:bool, **kwargs: Any) -> Dict:
    #     return {
    #         key: value for key, value in data.items() if type(value) not in self.SKIP_TYPES
    #     }