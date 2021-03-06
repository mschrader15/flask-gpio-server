from flask import Flask
from sources.SocketIO import add_socketio_handlers
from flask_socketio import SocketIO
from sources.dashboard import get_blueprint
from sources.threadedControl import HardwareIO
import os
import time
from threading import Thread
# from multiprocessing import Process

# for socketio you have to do this patch
from eventlet import wsgi


def spawn_hardware_thread():
    print('spawning hardware thread')
    hardware_control = HardwareIO('hardware', in_valve_pin=16, out_valve_pin=17)
    hardware_control.kill_event.set()
    t = Thread(target=hardware_control.run)
    t.start()
    return hardware_control


hardware_class = spawn_hardware_thread()


def create_app(register_blueprint=True):
    print('creating app')
    app = Flask(__name__)
    app.secret_key = os.urandom(42)
    if register_blueprint:
        app.register_blueprint(get_blueprint(hardware_class))
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
    # socketio.on_event('connect', dashboard_bp)
    return socketio, app


# creating the app and socketio
socketio, application = create_app()

# adding the socketio handlers
add_socketio_handlers(socketio, hardware_class)

# cre


if __name__ == '__main__':
    try:
        import eventlet
        eventlet.monkey_patch()
        print('Entry Point')
        wsgi.server(eventlet.listen(('', 8000)), application)
        # socketio.run(application, port=8000)
    finally:
        # Make sure to close the valves on a crash
        hardware_class.kill_event.set()
        time.sleep(2)
    # socketio.run(application, host='127.0.0.1', port='5000')
