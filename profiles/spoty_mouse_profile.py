from .default_profile import Profile
import evdev
from package import commands

KEY_DOWN = evdev.KeyEvent.key_down
KEY_UP = evdev.KeyEvent.key_up
KEY_HOLD = evdev.KeyEvent.key_hold

SHIFT_ENABLED = False

# event.type=1 event.code=272 event.value=1  RIGHT DOWN

def log(event: evdev.InputEvent):
    ignored_types = [0, 4]
    ignored_codes = [(2, 0), (2, 1), (2, 11)]
    if (
        event.type not in ignored_types
        and (event.type, event.code) not in ignored_codes
    ):
        print(evdev.categorize(event))
        print(f"{event.type=} {event.code=} {event.value=}")
        print("----------------------------")
    return None

# Volume Control
def scroll__shifted(event: evdev.InputEvent):
    value = event.value
    code = 115 if value > 0 else 114
    print(f'VOLUME {"UP" if code == 115 else "DOWN"}')
    return [
        commands.KeyCommand(code=code, value=1),
        commands.KeyCommand(code=code, value=0),
    ]

# Playlist Scroll
def scroll__main(event: evdev.InputEvent):
    value = event.value
    code = 103 if value > 0 else 108
    print(f'{"UP" if code == 103 else "DOWN"} ->')
    return [
        # ARROW KEY (code) DOWN
        commands.KeyCommand(code=code, value=1),
        # ARROW KEY (code) UP
        commands.KeyCommand(code=code, value=0),
    ]


def scroll(event: evdev.InputEvent):
    global SHIFT_ENABLED
    if SHIFT_ENABLED:
        return scroll__shifted(event)
    else:
        return scroll__main(event)

# Song Selection
def left_btn(event: evdev.InputEvent):
    value = event.value
    if value == KEY_DOWN:
        print('ENTER')
        return [
        # ENTER KEY DOWN
        commands.KeyCommand(code=28, value=1),
        # ENTER KEY UP
        commands.KeyCommand(code=28, value=0),
    ]

# Enable Shift
def right_btn(event: evdev.InputEvent):
    global SHIFT_ENABLED
    value = event.value
    if value == KEY_DOWN:
        SHIFT_ENABLED = True
        print(f'{SHIFT_ENABLED=}')
    if value == KEY_UP:
        SHIFT_ENABLED = False
        print(f'{SHIFT_ENABLED=}')
    return None

spoty_mouse = {
    "default": log,
    (2, 8): scroll,
    (1, 272): left_btn,
    (1,  273): right_btn,
}


class SpotyMouseProfile(Profile):
    mapping = spoty_mouse
