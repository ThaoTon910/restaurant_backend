# dto/payment.py
from attr import attrib, attrs, validators, Factory
from uuid import UUID, uuid4


@attrs
class PaymentDTO(object):
    payment_intent_id = attrib(
        init=True,
        type=str,
        validator=validators.instance_of(str),
    )
    client_secret = attrib(
        init=True,
        type=str,
        validator=validators.instance_of(str),
    )
    receipt_url = attrib(
        init=False,
        type=str,
        validator=validators.instance_of(str),
    )
    refunded = attrib(
        init=True,
        type=bool,
        default=False,
        validator=validators.instance_of(bool),
    )

    # order_id = attrib(
    #     init=True,
    #     type=UUID,
    #     validator=validators.instance_of(UUID),
    # )
