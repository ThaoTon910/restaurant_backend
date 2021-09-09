from marshmallow import Schema, EXCLUDE

def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)



class BaseSchema(Schema):
    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)

    class Meta:
        unknown = EXCLUDE
    # SKIP_TYPES = {type(None)} # set([type(None)])
    #
    # @post_dump
    # def remove_skip_types(self, data: Dict, many:bool, **kwargs: Any) -> Dict:
    #     return {
    #         key: value for key, value in data.items() if type(value) not in self.SKIP_TYPES
    #     }