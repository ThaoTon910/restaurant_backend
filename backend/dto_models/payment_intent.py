from attr import attrib, attrs, validators, Factory

@attrs
class PaymentIntentDTO(object):
    client_secret = attrib(
        init=True,
        type=str,
        validator=validators.instance_of(str),
    )
