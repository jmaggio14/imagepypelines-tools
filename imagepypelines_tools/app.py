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

from flask import Flask, flash, redirect, render_template, request, session, abort, g, jsonify
from flask_socketio import SocketIO, emit
import os
import json

from Chatroom import Chatroom

import pkg_resources
templates_dir = pkg_resources.resource_filename(__name__, 'templates/')
# dashboard_html_path = pkg_resources.resource_filename(__name__, 'templates/dashboard.html')
# login_html_path = pkg_resources.resource_filename(__name__, 'templates/login.html')
# index_html_path = pkg_resources.resource_filename(__name__, 'templates/layouts/index.html')

# CHATROOM_ACTIVE = False

app = Flask(__name__, template_folder=templates_dir)
app.debug = False
# note: use an environment variable - jb
app.secret_key = 'this_should_be_replaced_in_production!!!'
socketio = SocketIO(app, async_mode=async_mode, cors_allowed_origins="*")

host = '0.0.0.0'
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
    return render_template('dashboard.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/login/auth")
def auth(request):
    # follow tutorial for authentication of use Flask-Login plugin
    return render_template('layouts/index.html')   # this may need to change (should show base dashboard or first pipeline listed)

@app.route("/api/sessions")
def get_sessions():
    uuids = [v['uuid'] for v in c.sessions.values() if v is not None]
    for uuid in uuids:
        c.push(json.dumps({'uuid':uuid}))
    print(uuids)
    return jsonify(uuids)

# Helper for grabbing value out of chatroom's socket map using pipeline's uuid (could be expanded to other keys!!!)
# SHOULD BE MOVED TO CHATROOM OBJECT AS INSTANCE METHOD
def check_metadata(uuid):
    for v in c.sessions.values():
        if v is None:
            continue
        if v['uuid'] == uuid:
            return v
    return None

# Both of the following funcs need to be rewritten with respect to how sessions are mapped.
# We're trying to grab all 'cached' messages for a given pipeline by uuid and message type
# @app.route("/api/session/<uuid>/graph")
# def get_graph(uuid=None):
#     ids = [v['uuid'] for v in c.sessions.values() if v is not None]
#     if (uuid is None or uuid not in ids):
#         abort(404)
#
#     metadata = get_metadata(uuid)
#
#     if metadata is not None:
#         return jsonify(metadata[uuid]['graph'])
#     else:
#         abort(404)

# This new route should handle all requests for cached messages for any connected pipeline and any supported msg_type
@app.route("/api/session/<uuid>/<msg_type>")
def get_status(uuid=None, msg_type=None):
    ids = [v['uuid'] for v in c.sessions.values() if v is not None]
    if (uuid is None or uuid not in ids):
        abort(404)

    if (msg_type is None or msg_type not in ["graph", "status"]): # add other types here or use ip.MSG_TYPES (which we should add so people can hack on this!!!)
        abort(404)

    metadata = check_metadata(uuid)

    if metadata is not None:
        return jsonify(metadata[msg_type])
    else:
        abort(404)
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
@socketio.on('edit')
def edit(data):
    print(f"Editing graph for pipeline ID {data['PID']} of session ID {data['SID']}")
    send_to_chatroom(data)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0',port=5000)
    c.stop_thread()
