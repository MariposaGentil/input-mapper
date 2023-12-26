import evdev
import argparse

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


    def handle_args(self):
        self.args = vars(self.parser.parse_args())
        self.list = self.args.get('list', False)
        self.device_name = self.args.get('device_name', '')

    def list_devices(self, device_name):
        all_devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        devices = []
        for device in all_devices:
            if device_name.lower() in device.name.lower():
                print(f'Device found: {device.path}, {device.name}, {device.phys}')
                devices.append(device)
        return devices
    
    def get_device(self, device_name):
        devices = self.list_devices(device_name)
        assert len(devices) == 1
        return devices[0]

    def grap_device(self, device: evdev.InputDevice):
        for event in device.read_loop():
            print(evdev.categorize(event))
        
    def run(self):
        self.handle_args()
        if self.list:
            self.list_devices(self.device_name)
            return
        try:
            device = self.get_device(self.device_name)
            self.grap_device(device)
        except AssertionError:
            print('Could not select a device; probably zero or more than 1 device was returned')

if __name__ == '__main__':
    Main().run()