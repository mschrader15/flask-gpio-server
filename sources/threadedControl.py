import random
import time
from queue import Queue
from threading import Thread, Event
from datetime import datetime

DATE_FMT = "%Y-%m-%d %H:%M:%S"

OUTPUT_QUEUE = Queue()
INPUT_QUEUE = Queue()
KILL_EVENT = Event()

REFRESH_RATE = 1 # seconds

class HardwareIO:

    def __init__(self, name):
        self.name = name
        self.output_queue = OUTPUT_QUEUE
        self.input_queue = INPUT_QUEUE
        self.kill_event = KILL_EVENT

    def run(self):
        for fn in [self.implement_control, self.emit_readings]:
            t = Thread(target=fn)
            t.start()
        if self.kill_event.is_set():
            print('killed threads')
            t.join()

    def emit_readings(self):
        while not self.kill_event.is_set():
            timestamp = datetime.now().strftime(DATE_FMT)
            value = random.randint(0, 100)
            self._place_output({'x': [timestamp], 'y': [value]})
            time.sleep(REFRESH_RATE)

    def implement_control(self):
        while not self.kill_event.is_set():
            control = self._check_input()
            if control:
                self._take_action(control)
            time.sleep(REFRESH_RATE)

    def _check_input(self):
        if not self.input_queue.empty():
            print("Control Thread receive control: ", self.input_queue.get())
            return self.input_queue.get()

    def _place_output(self, value):
        self.output_queue.put(value)

    def _take_action(self, control):
        print(control)

