from app import app
from flask import request
from flask_socketio import SocketIO, send, emit, join_room, leave_room, close_room, rooms, disconnect
from app.socketio import socketio  

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run()