import evdev
import argparse

from package import system_repo
from package import device_repo
from package import commands
from profiles import dj_mouse_profile

class Main():
    def __init__(self):
        self.parser = argparse.ArgumentParser(
           prog='Input Remapper',
           description='Get a single input and remap its inputs to keyboard outputs',
        )
        self.parser.add_argument(
            '-d',
            '--device-name',
            type=str,
            default=''
        )
        self.parser.add_argument(
            '-l',
            '--list',
            action='store_true'
        )
        self.parser.add_argument(
            '-g',
            '--grab-device',
            help='Grab device inputs',
            action='store_true'
        )
        self.parser.add_argument(
            '-r',
            '--recognized',
            help='Print recognized commands by the profile file',
            action='store_true'
        )
        self.parser.add_argument(
            '-a',
            '--all',
            help='Print all commands received',
            action='store_true'
        )


    def handle_args(self):
        self.args = vars(self.parser.parse_args())
        self.list = self.args.get('list', False)
        self.device_name = self.args.get('device_name', '')
        self.grab = self.args.get('grab_device', False)
        self.recon = self.args.get('recognized', False)
        self.all = self.args.get('all', False)

    def grap_device(self, device: evdev.InputDevice, grab: bool):
        if grab:
            print('Grabbing device')
            device.grab()
        try:
            for event in device.read_loop():
                if self.all:
                    print(f'Device Command Received: {evdev.categorize(event)}')
        except:
            device.ungrab()
        
    def run(self):
        self.handle_args()
        if self.list:
            system_repo.list_devices(self.device_name)
            return
        try:
            device = system_repo.get_device(self.device_name)
        except AssertionError:
            print('Could not select a device; probably zero or more than 1 device was returned')
            
        device = device_repo.Device(device)
        profile = dj_mouse_profile.DjMouseProfile

        if self.grab:
            device.grab()
            
        OUT = system_repo.Output()
        for event in device.read():
            if self.all:
                print(f'Device Command Received: {evdev.categorize(event)}')
            parsed_event = device.parse(event, profile)
            parsed_events = [parsed_event] if not isinstance(parsed_event, list) else parsed_event
            if parsed_events:
                if self.recon:
                    print(f'Device Command Recognized: {evdev.categorize(event)}')

                OUT.execute_command(parsed_events)

                print(f'Device Command Parsed')
                for event in parsed_events:
                    print(parsed_event.__dict__)

                

if __name__ == '__main__':
    Main().run()