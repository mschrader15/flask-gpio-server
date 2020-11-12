import time
from queue import Queue
from threading import Thread, Event
from datetime import datetime
from sources.rpi import HydrogenSensor
from sources.rpi import SolenoidValve

DATE_FMT = "%Y-%m-%d %H:%M:%S"

OUTPUT_QUEUE = Queue()
INPUT_QUEUE = Queue()
KILL_EVENT = Event()

REFRESH_RATE = 1 # seconds


class HardwareIO:

    def __init__(self, name, in_valve_pin, out_valve_pin):
        self.name = name
        self.output_queue = OUTPUT_QUEUE
        self.input_queue = INPUT_QUEUE
        self.kill_event = KILL_EVENT
        self.hydrogen_sensor = HydrogenSensor()
        self.valves = [SolenoidValve('in_valve', in_valve_pin), SolenoidValve('out_valve', out_valve_pin)]

    def run(self):
        print('Hardware Starting')
        for fn in [self.implement_control, self.emit_readings]:
            t = Thread(target=fn)
            t.start()
        while True:
            time.sleep(REFRESH_RATE)
            if self.kill_event.is_set():
                for action in ('off_0', 'off_1'):
                    self._take_action(action)
                print('valves are off')

    def emit_readings(self):
        while not self.kill_event.is_set():
            timestamp, value = self.hydrogen_sensor.get_reading()
            self._place_output(['update', {'x': [timestamp.strftime(DATE_FMT)], 'y': [value]}])
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
        else:
            self.valves[int(valve)].close()
            print(control)

    def _emit_control(self):
        for valve in self.valves:
            self.output_queue.put(['valve_status', valve.status])


