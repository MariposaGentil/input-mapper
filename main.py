import evdev
import argparse
import atexit

from package import system_repo
from package import device_repo
from package import commands
from profiles import REGISTERED_PROFILES


class Main:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="Input Remapper",
            description="Get a single input and remap its inputs to keyboard outputs",
        )
        self.parser.add_argument("-d", "--device-name", type=str, default="")
        self.parser.add_argument("-l", "--list", action="store_true")
        self.parser.add_argument(
            "-g", "--grab-device", help="Grab device inputs", action="store_true"
        )
        self.parser.add_argument(
            "-r",
            "--recognized",
            help="Print recognized commands by the profile file",
            action="store_true",
        )
        self.parser.add_argument(
            "-a", "--all", help="Print all commands received", action="store_true"
        )
        self.parser.add_argument(
            "-p",
            "--profile",
            choices=REGISTERED_PROFILES.keys(),
            help="Profile to map inputs",
        )

    def handle_args(self):
        self.args = vars(self.parser.parse_args())
        self.list = self.args.get("list", False)
        self.device_name = self.args.get("device_name", "")
        self.grab = self.args.get("grab_device", False)
        self.recon = self.args.get("recognized", False)
        self.all = self.args.get("all", False)
        self.profile = self.args.get("profile", "")

    def get_profile(self):
        if not self.profile:
            return REGISTERED_PROFILES["DEFAULT_PROFILE"]
        else:
            return REGISTERED_PROFILES[self.profile]

    def run(self):
        self.handle_args()
        if self.list:
            system_repo.list_devices(self.device_name)
            return
        try:
            device = system_repo.get_device(self.device_name)
        except AssertionError:
            print(
                "Could not select a device; probably zero or more than 1 device was returned"
            )
            return 1

        device = device_repo.Device(device)
        profile = self.get_profile()

        if self.grab:
            device.grab()

        OUT = system_repo.Output()
        for event in device.read():
            if self.all:
                print(f"Device Command Received: {evdev.categorize(event)}")
            parsed_event = device.parse(event, profile)
            if not parsed_event:
                continue
            parsed_events = (
                [parsed_event] if not isinstance(parsed_event, list) else parsed_event
            )
            if parsed_events:
                if self.recon:
                    print(f"Device Command Recognized: {evdev.categorize(event)}")
                OUT.execute_command(parsed_events)


if __name__ == "__main__":
    Main().run()
