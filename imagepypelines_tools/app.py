"""
testing script for now, but this should probably end up as the driver for our app
~~~~~~~~~~~~

Things I'm going to do here:

1) Get a basic index.html displayed with correct bootstrap css theme

2) Figure out how to do form or radio button input client side and print it server side (or use it to update something css-y from server to client)

3) Display an image or array or graph using matplotlib and numpy
"""

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on available packages.
async_mode = None

if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()

from flask import Flask, flash, redirect, render_template, request, session, abort, g
from flask_socketio import SocketIO, emit
import os

from Chatroom import Chatroom

# CHATROOM_ACTIVE = False

app = Flask(__name__)
app.debug = False
app.secret_key = 'this_should_be_replaced_in_production!!!'
socketio = SocketIO(app, async_mode=async_mode)

host = 'localhost'
port = 9000 # THIS WILL BE CMD LINE ARGUMENT
c = Chatroom(host, port, socketio)
c.start()

# import atexit
# atexit.register(c.stop_thread)

################################################################################
# Basic Flask application funcs (html handling, rerouting, other basic web shit)
################################################################################
@app.route("/")
def welcome():
    return render_template("dashboard.html")

@app.route("/login")
def login():
    return render_template("login.html")


################################################################################
# Client generated event processors
################################################################################
def run_pipeline(data):

    return 0

def send_to_chatroom(data):

    # Not going to use websockets here most likely... Do I need TCP??? Or will a queue do? I have the chatroom reference here soooooooo
    pass

@socketio.on('connected')
def on_connect(msg):
    print(msg)

@socketio.on('run-start')
def run(data):
    print(f"Running pipeline ID {data['PID']} of session ID {data['SID']}...")
    msg = {'status': run_pipeline(data)}
    emit('run-finish', msg)

# For now, if anything changes at all for the task graph or blocks, send a full
#    update to the pipeline so everything is guaranteed to be in sync
@socketio.on('graph-change')
def edit(data):
    print(f"Editing graph for pipeline ID {data['PID']} of session ID {data['SID']}")
    send_to_chatroom(data)


if __name__ == '__main__':
    socketio.run(app, host='localhost',port=5000)
    c.stop_thread()
