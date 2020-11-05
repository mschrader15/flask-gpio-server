from flask import request
from sources.threadedControl import KILL_EVENT, INPUT_QUEUE, OUTPUT_QUEUE, HardwareIO
import time
from threading import Thread
from index import MESSAGE_QUEUE
from datetime import datetime

DATE_FMT = "%Y-%m-%d %H:%M:%S"

UPDATE_INTERVAL = 1

def _bootstrap_on_connect(socketio):
    socketio.emit('bootstrap', {'x': [datetime.now().strftime(DATE_FMT)], 'y': [0]})


def add_socketio_handlers(socketio):
    def _emit_event():
        while True:
            if not OUTPUT_QUEUE.empty():
                data = OUTPUT_QUEUE.get()
                print('fetched data', data)
                socketio.emit('update', OUTPUT_QUEUE.get(), broadcast=True)
            time.sleep(UPDATE_INTERVAL)

    @socketio.on('connect')
    def on_connect():
        KILL_EVENT.clear()
        print('connecting')
        _bootstrap_on_connect(socketio)
        for fn in [HardwareIO('hardware').run, _emit_event]:
            t = Thread(target=fn)
            t.start()

    @socketio.on('disconnect')
    def on_disconnect():
        KILL_EVENT.set()
        print('disconnect')

    @socketio.on('message')
    def on_message(message):
        INPUT_QUEUE.put(message)

    @socketio.on_error_default
    def default_error_handler(e):
        print(request.event["message"])  # "my error event"
        print(request.event["args"])





