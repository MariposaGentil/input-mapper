import evdev
import profiles
import atexit


class Device:
    def __init__(self, device: evdev.InputDevice):
        self.input = device
        self.grabbed = False

    def read(self):
        try:
            for event in self.input.read_loop():
                yield event
        except:
            self.ungrab()
            raise

    def grab(self):
        self.input.grab()
        self.grabbed = True
        atexit.register(self.ungrab)

    def ungrab(self):
        if self.grabbed:
            self.input.ungrab()

    def parse(self, event: evdev.InputEvent, profile: profiles.Profile):
        return profile.map(event)
