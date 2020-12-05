import time
from queue import Queue
from threading import Thread, Event
from datetime import datetime
from sources.rpi import HydrogenSensor
from sources.rpi import SolenoidValve
from index import REFRESH_RATE

DATE_FMT = "%Y-%m-%d %H:%M:%S.%f"


class HardwareIO:

    def __init__(self, name, in_valve_pin, out_valve_pin):
        self.clients = []
        self.name = name
        self.currently_off = True
        self.output_queue = Queue()
        self.input_queue = Queue()
        self.kill_event = Event()
        self.hydrogen_sensor = HydrogenSensor()
        self.valves = [SolenoidValve('in_valve', in_valve_pin), SolenoidValve('out_valve', out_valve_pin)]

    def run(self):
        print('Hardware Starting')
        # for fn in [self.implement_control, self.emit_readings]:
        for fn in [self.emit_readings]:
            t = Thread(target=fn)
            t.start()
        while True:
            time.sleep(REFRESH_RATE)
            if self.kill_event.is_set() and not self.currently_off:
                for action in ('off_0', 'off_1'):
                    self._take_action(action)
                self.currently_off = True
                print('valves are off')

    def emit_readings(self):
        while True:
            if not self.kill_event.is_set():
                timestamp, value = self.hydrogen_sensor.get_reading()
                # if self.record:
                self._place_output(['update', {'x': [timestamp.strftime(DATE_FMT)[:-3]], 'y': [value]}])
            time.sleep(REFRESH_RATE)

    def implement_control(self):
        # while not self.kill_event.is_set():
        while True:
            control = self._check_input()
            if control:
                self._take_action(control)
                self._emit_control()
            time.sleep(REFRESH_RATE)

    def _check_input(self):
        if not self.input_queue.empty():
            return self.input_queue.get()

    def _place_output(self, value):
        self.output_queue.put(value)

    def _take_action(self, control):
        on_off, valve = control.split('_')
        if on_off == 'on':
            self.valves[int(valve)].open()
            print(control)
            self.currently_off = False
        else:
            self.valves[int(valve)].close()
            print(control)

    def _emit_control(self):
        for valve in self.valves:
            self.output_queue.put(['valve_status', "_".join([valve.name, valve.status])])

    def control_valve(self, num, action):
        print(num, action)
        if action == 'open':
            self.valves[num].open()
            self.currently_off = False
        else:
            self.valves[num].close()


