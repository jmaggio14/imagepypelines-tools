import subprocess
import sys
import argparse
import docker

from ..app import app, socketio, chatroom
from .util import check_docker
from .. import DASHBOARD_LATEST_TAG, DASHBOARD_VERSION_TAG


DEFAULT_DASHBAORD_IP = "0.0.0.0"
DEFAULT_DASHBOARD_PORT = 5000
DEFAULT_CHATROOM_PORT = 9000

def dashboard(parser=None, args=None):
    """launches the dashboard"""
    # ideas for additonal flags (I just chose explicit names for now -JM)
    #
    # --timeout  --> timeout if no pipelines or clients connect to it
    # --from_file --> pulls config from a file
    # --restricted_access --> something for restricted access
    if not parser:
        parser = argparse.ArgumentParser()

    parser.add_argument("host",
                        help="IP address of the dashboard server to ping",
                        nargs='?',
                        default=DEFAULT_DASHBAORD_IP,
                        type=str)
    parser.add_argument("port",
                        help="port number of the dashboard",
                        nargs='?',
                        default=DEFAULT_DASHBOARD_PORT,
                        type=int)
    parser.add_argument('-c',
                        "--chatroom-port",
                        help="port number of the dashboard",
                        default=DEFAULT_CHATROOM_PORT,
                        type=int)
    parser.add_argument("--containerized",
                        help="whether or not to launch the dashboard in a docker container. Requires docker to be installed.",
                        action='store_true')
    parser.add_argument("--latest",
                        help="only applies if --containerized is used. whether or not to force the most recent image to be used",
                        action='store_true')
    parser.add_argument("--stop",
                        help="only applies if --containerized was used. stops the currently running dashboard container (name = 'ip-dashboard')",
                        action='store_true')

    args = parser.parse_args()

    # Check to see if we're just stopping the running dashboard
    if args.stop:
        client = docker.from_env()
        client.containers.get("ip-dashboard").stop()
        # Right now we stop and then immediately remove
        # Maybe in the future we want to allow starting instead of always running? Need to brush up on behavior here
        client.containers.get("ip-dashboard").remove()

    else:

        print(f"Dashboard launching at {args.host}:{args.port}...")

        if args.containerized:
            CONTAINERIZED = True
            # _docker_dashboard(parser,args)
            _docker_dashboard(parser,args)

        else:
            # this will be switched to execution using Gevent or WSGI (link from Jai)
            # https://flask.palletsprojects.com/en/1.1.x/deploying/wsgi-standalone/

            # start up the chatroom in its own thread)
            print("Chatroom launching...")
            chatroom.start()

            # launch the socketio app and BLOCK!!!
            socketio.run(app, host=args.host, port=args.port)

            # once run command above finishes, stop the chatroom thread too
            chatroom.stop_thread()

            # print out a nice message (We should make this the copyright or something)
            print("\nThank you for choosing ImagePypelines. See you next time!")

def _docker_dashboard(parser, args):
    """launches the dashboard"""
    # ideas for additonal flags (I just chose explicit names for now -JM)
    #
    # --timeout  --> timeout if no pipelines or clients connect to it
    # --from_file --> pulls config from a file
    # --restricted_access --> something for restricted access
    check_docker()

    tag = DASHBOARD_VERSION_TAG
    if args.latest:
        tag = DASHBOARD_LATEST_TAG

    # Do the same thing as above, but using docker client library to run container!
    client = docker.from_env()
    worker = client.containers.run(tag, name="ip-dashboard", ports={args.port:DEFAULT_DASHBOARD_PORT, args.chatroom_port:DEFAULT_CHATROOM_PORT}, detach=True)
    # could return the worker to an IP registry of containers or something


# def _docker_dashboard(parser, args):
#     """launches the dashboard"""
#     # ideas for additonal flags (I just chose explicit names for now -JM)
#     #
#     # --timeout  --> timeout if no pipelines or clients connect to it
#     # --from_file --> pulls config from a file
#     # --restricted_access --> something for restricted access
#     check_docker()
#
#     tag = DASHBOARD_VERSION_TAG
#     if args.latest:
#         tag = DASHBOARD_LATEST_TAG
#
#     cmd = ['docker',
#             'run',
#             '-p', f'{args.port}:{DEFAULT_DASHBOARD_PORT}',
#             '-p', f'{args.chatroom_port}:{DEFAULT_CHATROOM_PORT}',
#             tag]
#
#     subprocess.run(cmd)
