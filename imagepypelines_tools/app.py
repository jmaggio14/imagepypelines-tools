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
import networkx as nx

app = Flask(__name__, template_folder='site', static_folder='site')
app.debug = True
socketio = SocketIO(app)

# cache_exists = os.path.exists(default_cache_dir)
# default_cache_dir = os.path.join(os.path.expanduser('~'),'.imagepypelines')


@app.route("/")
def welcome():
    return render_template("templates/sampleapplet.html")

@socketio.on('enter prog bar width')
def progress(data):
    print("Here's our width:   ", data['width'])
    msg = {'width': data['width']}
    emit('return prog bar width', msg)



if __name__ == '__main__':
    socketio.run(app, host='localhost',port=5000)
