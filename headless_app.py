import eventlet
import socketio
from sources.SocketIO import add_socketio_handlers

sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio)

add_socketio_handlers(sio, flask=False)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
