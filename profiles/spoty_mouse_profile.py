from .default_profile import Profile
import evdev
from package import commands

RIGHT_CLICK_DOWN = False
LEFT_CLICK_DOWN = False
RIGHT_CLICK_UP = False
LEFT_CLICK_UP = False


def default(event: evdev.InputEvent):
    ignored_types = [0]
    ignored_codes = [(2, 0), (2, 1)]
    if (
        event.type not in ignored_types
        and (event.type, event.code) not in ignored_codes
    ):
        print(evdev.categorize(event))
        print(f"{event.type=} {event.code=} {event.value=}")
        print("----------------------------")
    return None


def scroll(event: evdev.InputEvent):
    value = event.value
    up = value > 0
    return [
        commands.KeyCommand(code=103 if up else 108, value=1),
        commands.KeyCommand(code=103 if up else 108, value=0),
    ]


spoty_mouse = {
    "default": default,
    (2, 8): scroll,
    # (2, 11)='SCROLL UP',
}


class SpotyMouseProfile(Profile):
    mapping = spoty_mouse
