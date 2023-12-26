from . import Profile
import evdev
from package import commands

NEXT_VALUE = evdev.KeyEvent.key_up


def default(event: evdev.InputEvent):
    global NEXT_VALUE
    value = NEXT_VALUE
    to_ret = commands.KeyCommand(
        code=evdev.ecodes.KEY_A,
        value=value,
    )
    NEXT_VALUE = (
        evdev.KeyEvent.key_down
        if value == evdev.KeyEvent.key_up
        else evdev.KeyEvent.key_up
    )
    return to_ret


dj_mouse = dict(default=default)


class DjMouseProfile(Profile):
    mapping = dj_mouse
