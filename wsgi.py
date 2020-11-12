from app import application, socketio
from eventlet import wsgi
import eventlet

# This monkey patch is necessary to work
# from gevent import monkey
# monkey.patch_all()

if __name__ == "__main__":
    wsgi.server(eventlet.listen(('', 5000), socketio.run(application)))
