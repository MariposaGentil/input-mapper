import evdev
import re

import typing


def copy_event(event: evdev.InputEvent):
    return event

no_mapping = {'default': copy_event}

class Profile:
    mapping = no_mapping

    @classmethod
    def map(cls, event: evdev.InputEvent):
        mapped_object = cls._get_mapping(event.code)
        if not mapped_object:
            return None
        if isinstance(mapped_object, evdev.InputEvent):
            return mapped_object
        if isinstance(mapped_object, typing.Callable):
            return mapped_object(event)
        
    
    @classmethod
    def _get_mapping(cls, event_code: str):
        if event_code in cls.mapping:
            return cls.mapping[event_code] 
        
        for key in cls.mapping.keys():
            if isinstance(key, re.Pattern):
                if key.search(event_code):
                    return cls.mapping[key]
    
        if 'default' in cls.mapping:
            return cls.mapping['default']
        
        return None
        

