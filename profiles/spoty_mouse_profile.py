from .default_profile import Profile
import evdev
from package import commands

KEY_DOWN = evdev.KeyEvent.key_down
KEY_UP = evdev.KeyEvent.key_up
KEY_HOLD = evdev.KeyEvent.key_hold

# event.type=1 event.code=272 event.value=1  RIGHT DOWN

def log(event: evdev.InputEvent):
    ignored_types = [0]
    ignored_codes = [(2, 0), (2, 1), (2, 11)]
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
    code = 103 if value > 0 else 108
    return [
        # ARROW KEY DOWN
        commands.KeyCommand(code=code, value=1),
        # ARROW KEY UP
        commands.KeyCommand(code=code, value=0),
    ]

def left_btn(event: evdev.InputEvent):
    value = event.value
    if value == KEY_DOWN:
        return [
        # ENTER KEY DOWN
        commands.KeyCommand(code=28, value=1),
        # ENTER KEY UP
        commands.KeyCommand(code=28, value=0),
    ]
        

spoty_mouse = {
    "default": log,
    (2, 8): scroll,
    (1, 272): left_btn
}


class SpotyMouseProfile(Profile):
    mapping = spoty_mouse
