from app import application, socketio
from eventlet import wsgi
import eventlet

if __name__ == "__main__":
    wsgi.server(eventlet.listen(('', 5000), socketio.run(application)))
