from attr import attrib, attrs, validators
from datetime import datetime
from typing import List
from ._base import AsDict

@attrs
class HourDTO(AsDict):

    start = attrib(
        init=True,
        type=datetime,
    )

    end = attrib(
        init=True,
        type=datetime,
    )

    day = attrib(
        init=True,
        type=str,
        validator=validators.in_(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),
    )

    off = attrib(
        init=True,
        type=bool,
        default=False,
        validator=validators.instance_of(bool),
    )



def check_hours(cls, attribute, value: List[HourDTO]):

    if not len(value) == 7:
        raise ValueError("Must have hours for 7 days")
    days = {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'}
    input_days = set()
    for v in value:
        input_days.add(v.day)
    diff = days - input_days
    if len(diff):
        raise ValueError("Missing {}".format(str(diff)))