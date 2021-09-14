# dto_models/customer.py
from attr import attrib, attrs, validators, Factory
from uuid import UUID, uuid4
from datetime import datetime


@attrs
class CustomerDTO(object):
    first_name = attrib(
        init=True,
        type=str,
        validator=validators.instance_of(str)
    )
    last_name = attrib(
        init=True,
        type=str,
        validator=validators.instance_of(str)
    )
    phone_number = attrib(
        init=True,
        type=str,
        validator=validators.instance_of(str)
    )
    email = attrib(
        init=True,
        type=str,
        validator=validators.instance_of(str)
    )
    # street = attrib(
    #     init=True,
    #     type=str,
    #     validator=validators.instance_of(str)
    # )
    # city = attrib(
    #     init=True,
    #     type=str,
    #     validator=validators.instance_of(str)
    # )
    # state = attrib(
    #     init=True,
    #     type=str,
    #     validator=validators.instance_of(str)
    # )
    # zipcode = attrib(
    #     init=True,
    #     type=int,
    #     validator=validators.instance_of(int)
    # )
    # reward_point = attrib(
    #     init=True,
    #     type=int,
    #     validator=validators.instance_of(int)
    # )
    # created_time = attrib(
    #     init=False,
    #     type=datetime,
    #     default=Factory(datetime.utcnow),
    #     validator=validators.instance_of(datetime)
    # )
    # id = attrib(
    #     type=UUID,
    #     default=Factory(uuid4),
    #     validator=validators.instance_of(UUID)
    # )
