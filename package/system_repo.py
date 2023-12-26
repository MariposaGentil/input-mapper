import evdev
from package.commands import Command
from package.device_repo import Device
import atexit


def list_devices(search_term: str) -> [evdev.InputDevice]:
    all_devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    devices = []
    for device in all_devices:
        if (
            search_term.lower() in device.name.lower()
            or search_term.lower() in device.path.lower()
        ):
            print(f"Device found: {device.path}, {device.name}, {device.phys}")
            devices.append(device)
    return devices


def get_device(device_name: str) -> evdev.InputDevice:
    devices = list_devices(device_name)
    assert len(devices) == 1
    return devices[0]


def get_keyboard_device() -> evdev.InputDevice:
    dev = get_device("AT Translated Set 2 keyboard")
    return evdev.UInput.from_device(dev, name="input-remapper-kbdremap")


class Output:
    def __init__(self):
        self.OUT = get_keyboard_device()
        atexit.register(self.OUT.close)

    def execute_command(self, events: list[Command]):
        for event in events:
            self.OUT.write(event.type, event.code, event.value)
        self.OUT.syn()
