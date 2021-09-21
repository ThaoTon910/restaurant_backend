# schemas/order_item.py
from marshmallow import fields
from schemas import BaseSchema


class OrderItemSchema(BaseSchema):
    # Resource
     menuItemId = fields.UUID(required=True, attribute="menu_item_id")
     quantity = fields.Integer(required=True)
     addOns = fields.List(fields.UUID, required=False, attribute="add_ons")
     specialInstruction = fields.String(required=False, attribute="special_instruction")
     price = fields.Float(required=True, dump_only=True)




