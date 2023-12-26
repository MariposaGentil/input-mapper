import evdev


class Command:
    def __init__(self, type: int, code: int, value: int):
        self.type = type
        self.code = code
        self.value = value


class KeyCommand(Command):
    def __init__(self, code: int, value: int):
        super().__init__(evdev.ecodes.EV_KEY, code, value)
