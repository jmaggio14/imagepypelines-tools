"""
testing script for now, but this should probably end up as the driver for our app
~~~~~~~~~~~~

Things I'm going to do here:

1) Get a basic index.html displayed with correct bootstrap css theme

2) Figure out how to do form or radio button input client side and print it server side (or use it to update something css-y from server to client)

3) Display an image or array or graph using matplotlib and numpy
"""

from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_socketio import SocketIO, emit
import os

from Chatroom import Chatroom

# CHATROOM_ACTIVE = False

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)

host = 'localhost'
port = 5050 # THIS WILL BE CMD LINE ARGUMENT
c = DashboardChatroom(host, port, socketio) # this func needs to kick off Chatroom instance in it's own thread
c.start()

################################################################################
# Basic Flask application funcs (html handling, rerouting, other basic web shit)
################################################################################
@app.route("/")
def welcome():
    return render_template("sampleapplet.html")

################################################################################
# Client generated event processors
################################################################################
def run_pipeline(data):

    return 0

def send_to_chatroom(data):

    # Not going to use websockets here most likely... Do I need TCP??? Or will a queue do? I have the chatroom reference here soooooooo
    pass

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
