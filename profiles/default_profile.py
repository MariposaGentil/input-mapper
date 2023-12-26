import evdev
import re
from package.commands import Command

import typing


def copy_event(event: evdev.InputEvent):
    return Command(
        type=event.type,
        code=event.code,
        value=event.value,
    )


no_mapping = {"default": copy_event}


class Profile:
    mapping = no_mapping

    @classmethod
    def map(cls, event: evdev.InputEvent):
        mapped_object = cls._get_mapping(event.type, event.code)  # type: ignore
        if not mapped_object:
            return None
        if isinstance(mapped_object, evdev.InputEvent):
            return mapped_object
        if isinstance(mapped_object, typing.Callable):  # type: ignore
            return mapped_object(event)

    @classmethod
    def _get_mapping(cls, event_type: int, event_code: int):
        if (event_type, event_code) in cls.mapping:
            return cls.mapping[(event_type, event_code)]  # type: ignore

        for key in cls.mapping.keys():
            if isinstance(key, re.Pattern):
                if key.search(event_code):
                    return cls.mapping[key]

        if "default" in cls.mapping:
            return cls.mapping["default"]

        return None
