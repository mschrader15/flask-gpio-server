import time
from threading import Thread
# from multiprocessing import Process
from datetime import datetime
from flask import request
from index import REFRESH_RATE

REFRESH_RATE = REFRESH_RATE / 2

DATE_FMT = "%Y-%m-%d %H:%M:%S"


def _bootstrap_on_connect(socketio):

    socketio.emit('bootstrap', {'x': [datetime.now().strftime(DATE_FMT)], 'y': [0]})


def add_socketio_handlers(socketio, hardware_class, flask=True):

    def _emit_event(output_queue):
        while True:
            if not output_queue.empty():
                data = output_queue.get()
                emit_name = 'update' if data[0] == 'update' else 'reply-message'
                # emit_data =
                socketio.emit(emit_name, data[1:][0])
            time.sleep(REFRESH_RATE)

    if flask:

        @socketio.on('connect')
        def on_connect():
            hardware_class.clients.append(request.sid)
            print(request.sid)
            hardware_class.kill_event.clear()
            print('connecting')
            _bootstrap_on_connect(socketio)
            t = Thread(target=_emit_event, args=(hardware_class.output_queue, ))
            t.start()

        @socketio.on('disconnect')
        def on_disconnect():
            while request.sid in hardware_class.clients:
                hardware_class.clients.remove(request.sid)
            print('disconnect')
            if len(hardware_class.clients) < 1:
                print('last listener disconnected. sleeping hardware')
                hardware_class.kill_event.set()

        @socketio.on('message')
        def on_message(message):
            hardware_class.input_queue.put(message)

    # @socketio.on_error_default
    # def default_error_handler(e):
    #     print(request.event["message"])  # "my error event"
    #     print(request.event["args"])





