from flask import Flask
from sources.SocketIO import add_socketio_handlers
from flask_socketio import SocketIO
from sources.dashboard import dashboard_bp
from sources.threadedControl import HardwareIO
import os
import time
from threading import Thread
from index import MESSAGE_QUEUE

# for socketio
from eventlet import wsgi
import eventlet
eventlet.monkey_patch()


def create_app(register_blueprint=True):
    app = Flask(__name__)
    app.secret_key = os.urandom(42)
    if register_blueprint:
        app.register_blueprint(dashboard_bp)
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
    # socketio.on_event('connect', dashboard_bp)
    return socketio, app


def spawn_hardware_thread():
    hardware_control = HardwareIO('hardware', in_valve_pin=16, out_valve_pin=17)
    t = Thread(target=hardware_control.run)
    t.start()
    return hardware_control


socketio, application = create_app()
add_socketio_handlers(socketio)

hardware_class = spawn_hardware_thread()

if __name__ == '__main__':
    try:
        wsgi.server(eventlet.listen(('', 8000)), application)
    finally:
        # Make sure to close the valves on a crash
        hardware_class.kill_event.set()
        time.sleep(2)
    # socketio.run(application, host='127.0.0.1', port='5000')
