# converters/order_convert.py

from dbo_models.order_dbo import OrderDBO
from dto_models.app_order_dto import OrderDTO
from dto_models.customer import CustomerDTO
from dto_models.order_item import OrderItemDTO
from dto_models.payment import PaymentDTO

def order_dbo_to_dto(dbo: OrderDBO) -> OrderDTO:
    print("Inisde order_dbo_to_dto:  ", dbo.payment)
    customer = CustomerDTO(
        first_name=dbo.customer.first_name,
        last_name=dbo.customer.last_name,
        phone_number=dbo.customer.phone_number,
        email=dbo.customer.email,
    )
    customer.id = dbo.customer.id
    
    payment = {}
    if dbo.payment[0]:
        payment_dbo = dbo.payment[0]
        payment = PaymentDTO(
            payment_intent_id=payment_dbo.payment_intent_id,
            client_secret=payment_dbo.client_secret,
            refunded=payment_dbo.refunded
        )
        payment.receipt_url = payment_dbo.receipt_url

    items = [
        OrderItemDTO(
            special_instruction=order_item_dbo.special_instruction,
            quantity=order_item_dbo.quantity,
            menu_item_id=order_item_dbo.menu_item_id,
            add_ons=[
                addon.id for addon in order_item_dbo.add_ons
            ],
            price=order_item_dbo.price
        ) for order_item_dbo in dbo.order_items
    ]
    delivery = {}

    print("DELIVERY", dbo.delivery)
    if dbo.delivery:
        delivery_dbo = dbo.delivery[0]
        delivery = {
            "delivery_fee": delivery_dbo.fee,
            "info": {
                "delivery_type": delivery_dbo.delivery_type,
            }
        }
        if delivery_dbo.pick_up:
            delivery["info"]["time"] = delivery_dbo.pick_up.time
            delivery["info"]["merchant_id"] = delivery_dbo.pick_up.merchant_id


    dto = OrderDTO(
        promo_code=dbo.promo_code,
        tax_multiplier=dbo.tax_multiplier,
        tip_multiplier=dbo.tip_multiplier,
        customer=customer,
        items=items,
        delivery=delivery,
        id=dbo.id
    )
    dto.payment = payment
    dto.discount = dbo.discount
    dto.status = dbo.status

    # # Only take DTO attribute that has init=True
    dto.updated_time = dbo.updated_time
    dto.created_time = dbo.created_time
    # dto.id = dbo.id
    # if dbo.addon_groups:
    #     dto.addon_group_ids = [addon_group_dbo_to_dto(ag_dbo).id for ag_dbo in dbo.addon_groups]
    # else:
    #     dto.addon_group_ids = []
    return dto

