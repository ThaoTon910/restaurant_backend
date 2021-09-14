# converters/order_convert.py

from dbo_models.order_dbo import OrderDBO
from dto_models.app_order_dto import OrderDTO
from dto_models.customer import CustomerDTO
from dto_models.order_item import OrderItemDTO

def order_dbo_to_dto(dbo: OrderDBO) -> OrderDTO:
    customer = CustomerDTO(
        first_name=dbo.customer.first_name,
        last_name=dbo.customer.last_name,
        phone_number=dbo.customer.phone_number,
        email=dbo.customer.email
    )
    items = [
        OrderItemDTO(
            special_instruction=order_item_dbo.special_instruction,
            quantity=order_item_dbo.quantity,
            menu_item_id=order_item_dbo.menu_item.id,
            add_ons=[
                addon.id for addon in order_item_dbo.add_ons
            ]
        ) for order_item_dbo in dbo.order_items
    ]
    delivery = {"delivery_type": "pickup"}

    dto = OrderDTO(
        payment_token=dbo.payment_token,
        promo_code=dbo.promo_code,
        tax_multiplier=dbo.tax_multiplier,
        tip_multiplier=dbo.tip_multiplier,
        customer=customer,
        items=items,
        delivery=delivery,
        id=dbo.id
    )

    dto.discount = dbo.discount
    dto.status = dbo.status

    # # Only take DTO attribute that has init=True
    # dto.updated_time = dbo.updated_time
    # dto.created_time = dbo.created_time
    # dto.id = dbo.id
    # if dbo.addon_groups:
    #     dto.addon_group_ids = [addon_group_dbo_to_dto(ag_dbo).id for ag_dbo in dbo.addon_groups]
    # else:
    #     dto.addon_group_ids = []
    return dto

