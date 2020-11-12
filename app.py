from flask import Flask
from sources.SocketIO import add_socketio_handlers
from flask_socketio import SocketIO
from sources.dashboard import dashboard_bp
import os
from index import MESSAGE_QUEUE


def create_app(register_blueprint=True):
    app = Flask(__name__)
    app.secret_key = os.urandom(42)
    if register_blueprint:
        app.register_blueprint(dashboard_bp)
    socketio = SocketIO(app, cors_allowed_origins="*")
    # socketio.on_event('connect', dashboard_bp)
    return socketio, app


socketio, application = create_app()

add_socketio_handlers(socketio)

if __name__ == '__main__':
    socketio.run(application, host='127.0.0.1', port='5000')
