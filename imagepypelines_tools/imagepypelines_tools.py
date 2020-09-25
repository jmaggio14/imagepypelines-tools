# #!/usr/bin/env python
#
#
# """
#     1) Launch the Dashboard server
#         $ imagepypelines dashboard
#
#     2) Test ping a Dashboard server
#         $ imagepypelines ping <ip address> <port> [-i, --interval] [--no-repeat]
#
#     3) Running the imagepypelines shell:
#         $ imagepypelines shell
#         $ imagepypelines shell --gpu                     # (GPU - nvidia-docker required)
#         $ imagepypelines shell -v /host/path:/mount/path # (additonal volumes)
#         $ imagepypelines shell --nest                    # (force nested containers)
#
#     4) Rebuilding the imagepypelines docker images for this version
#         $ imagepypelines build
#         (no cache)
#         $ imagepypelines build --no-cache
#
#     5) Pulling the imagepypelines docker images from dockerhub
#         $ imagepypelines pull
#
#
# imagepypelines {shell, push, pull, dashboard, ping}
# """
#
# import argparse
# import os
# import subprocess
# from subprocess import DEVNULL
# import importlib
# import sys
# import pathlib
# import sys
# import pkg_resources
# import urllib.request
# import warnings
# import time
#
# from .version_info import __version__
# from . import BUILD_DIR, DOCKERFILES
#
# WORKING_DIR = os.path.abspath( os.getcwd() )
# drive = pathlib.Path(WORKING_DIR).drive
#
#
# if drive != '':
#     POSIX_PATH = WORKING_DIR.replace(drive, '/root').replace(os.sep, '/')
# else:
#     POSIX_PATH = os.path.join('/root', WORKING_DIR).replace(os.sep, '/')
#
#
# FLASK_APP = pkg_resources.resource_filename(__name__, "app.py")
#
# # BASE_TAGS = ['imagepypelines/imagepypelines-tools:dashboard']
# # TAGS = [tag + '-%s' % __version__ for tag in BASE_TAGS]
# # UPDATE_TAGS = ["imagepypelines/imagepypelines-tools:latest"]
# # HOSTNAMES = ['dashboard']
# # REGISTRY_URL = "https://registry.hub.docker.com/v1/repositories/imagepypelines/imagepypelines-tools/tags"
#
#
#
# GENERAL_DASHBOARD_TAG = 'imagepypelines/imagepypelines-tools:dashboard'
# # this tags the dashboard version to this version of iptools if it's built
# VERSION_DASHBOARD_TAG = f"{GENERAL_DASHBOARD_TAG}-{__version__}"
#
# CHATROOM_PORT = 9000
# DASHBOARD_PORT = 5000
#
#
#
# ################################################################################
# def docker_dashboard(parser, args):
#     """launches the dashboard in a docker container"""
#     check_docker('docker','--version')
#
#     parser.add_argument('dashboard-port',
#                         help='rebuilds the docker images without a cache',
#                         type=int,
#                         required=True)
#
#     parser.add_argument('chatroom-port',
#                         help='rebuilds the docker images without a cache',
#                         type=int,
#                         required=True)
#
#
#
#     args = parser.parse_args()
#
#     cmd = ['docker',
#             'run',
#             '--rm',
#             '-p', f"{args.chatroom_port}:{CHATROOM_PORT}",
#             '-p', f"{args.dashboard_port}:{DASHBOARD_PORT}",
#             DASH,
#             ]
#
#
#
# ################################################################################
# def ping(parser, args):
#     """spins up a test pipeline to communicate to the given dashboard"""
#     parser.add_argument("host",
#                         help="IP address of the dashboard server to ping",
#                         type=str)
#     parser.add_argument("port",
#                         help="port number of the dashboard",
#                         type=int)
#     parser.add_argument("-i", "--interval",
#                         help="interval in milliseconds to ping the dashboard",
#                         default=1000,
#                         type=int)
#     parser.add_argument("--no-repeat",
#                         help="flag whether or not to repeat this ping",
#                         action="store_true")
#     args = parser.parse_args()
#
#
#     # import imagepypelines in a try-catch for verbose error handling
#     try:
#         try:
#             import imagepypelines as ip
#             ip.set_log_level(100)
#         except ImportError:
#             print("unable to import ImagePypelines - it must be installed separately. Try \"pip install imagepypelines\"")
#             raise
#
#         # build the pipeline
#         pipeline = make_ping_pipeline()
#
#         # build internal helper function to connect to the dash and run the pipeline
#         def connect_and_run():
#             if ip.n_dashboards() == 0:
#                 ip.connect_to_dash('test_dash', args.host, args.port)
#                 # print message if we connect or fail to connect
#                 if ip.n_dashboards() == 0:
#                     if args.no_repeat:
#                         msg = f"unable to connect."
#                     else:
#                         msg = f"unable to connect... retrying in {args.interval}ms"
#                     print(msg)
#                 else:
#                     print("connection success!")
#
#             if ip.n_dashboards():
#                 print("pinging...")
#                 pipeline.process(list(range(10)), list(range(10)) )
#
#             time.sleep(args.interval / 1000)
#
#         # connect
#         if args.no_repeat:
#             connect_and_run()
#         else:
#             while True:
#                 connect_and_run()
#
#     except KeyboardInterrupt:
#         exit(0)
#
#
# ################################################################################
# # def push(parser, args):
# #     """pushes the docker images to dockerhub - DEVS ONLY"""
# #     print("Warning: \"push\" is only for imagepypelines developers")
# #     print("Warning: You must be manually logged into docker for this to complete successfully")
# #     # check if docker is installed
# #     check_docker('docker','--version')
# #
# #     # check if the tags we are pushing already exist on the repo
# #     # this is a little non-intuitive, but basically this fetches
# #     # a json string that convienently can be evaled into a python list
# #     # that contains all the tags we have on our repo
# #     response = urllib.request.urlopen(REGISTRY_URL).read().decode('utf-8')
# #     remote_tags = [tag['name'] for tag in eval(response,{},{})]
# #     local_tags = [t.split(':')[1] for t in TAGS]
# #
# #     # loop through all tags
# #     for full_tag, local in zip(TAGS, local_tags):
# #         # if this tags exists remotely, then we abort the push
# #         if local in remote_tags:
# #             print("error: {} exists remotely, skipping push!".format(local))
# #         else:
# #             print("attempting to push image {}".format(full_tag))
# #             subprocess.call(["docker", "push", full_tag])
#
# ################################################################################
#
#
# ################################################################################
# # ENTRY POINT
# def main():
#     # parsing command line arguments
#     parser = argparse.ArgumentParser(prog='imagepypelines',
#                                         usage=__doc__)
#
#     # primary argument
#     parser.add_argument('action',
#                         help="the primary action to perform",
#                         # define acceptable commands
#                         choices=["shell",
#                                     "push",
#                                     "pull",
#                                     "build",
#                                     "dashboard",
#                                     'ping',
#                                     ]
#                         )
#
#     args = parser.parse_known_args()[0]
#
#     ############################################################################
#     elif args.action == "build":
#         build(parser, args)
#
#     ############################################################################
#     elif args.action == "pull":
#         pull(parser, args)
#
#     ############################################################################
#     elif args.action == "dashboard":
#         dashboard(parser, args)
#
#     ############################################################################
#     elif args.action == "ping":
#         ping(parser, args)
#
#
# if __name__ == "__main__":
#     main()
#
# # END
