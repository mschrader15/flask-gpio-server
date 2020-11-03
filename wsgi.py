from app import application, socketio
# This monkey patch is necessary to work
from gevent import monkey
monkey.patch_all()

if __name__ == "__main__":
    socketio.run(application)
