#!/usr/bin/env python


"""
    1) Launch the Dashboard server
        $ imagepypelines dashboard

    2) Test ping a Dashboard server
        $ imagepypelines ping <ip address> <port> [-i, --interval] [--no-repeat]

    3) Running the imagepypelines shell:
        $ imagepypelines shell
        $ imagepypelines shell --gpu                     # (GPU - nvidia-docker required)
        $ imagepypelines shell -v /host/path:/mount/path # (additonal volumes)
        $ imagepypelines shell --nest                    # (force nested containers)

    4) Rebuilding the imagepypelines docker images for this version
        $ imagepypelines build
        (no cache)
        $ imagepypelines build --no-cache

    5) Pulling the imagepypelines docker images from dockerhub
        $ imagepypelines pull


imagepypelines {shell, push, pull, dashboard, ping}
"""

import argparse
import os
import subprocess
from subprocess import DEVNULL
import importlib
import sys
import pathlib
import sys
import pkg_resources
import urllib.request
import warnings
import time

from .version_info import __version__
from . import BUILD_DIR, DOCKERFILES

WORKING_DIR = os.path.abspath( os.getcwd() )
drive = pathlib.Path(WORKING_DIR).drive


if drive != '':
    POSIX_PATH = WORKING_DIR.replace(drive, '/root').replace(os.sep, '/')
else:
    POSIX_PATH = os.path.join('/root', WORKING_DIR).replace(os.sep, '/')


FLASK_APP = pkg_resources.resource_filename(__name__, "app.py")

DEFAULT_VOLUMES = ['{0}:{1}'.format(WORKING_DIR, POSIX_PATH)]
BASE_TAGS = ['imagepypelines/imagepypelines-tools:base',
                'imagepypelines/imagepypelines-tools:gpu']
TAGS = [tag + '-%s' % __version__ for tag in BASE_TAGS]
UPDATE_TAGS = ["imagepypelines/imagepypelines-tools:latest",
                "imagepypelines/imagepypelines-tools:latest-gpu"]
HOSTNAMES = ['imagepypelines', 'imagepypelines-gpu']
REGISTRY_URL = "https://registry.hub.docker.com/v1/repositories/imagepypelines/imagepypelines-tools/tags"
################################################################################
#                                   UTIL
################################################################################
def check_docker(command,ver="--version"):
    """runs a system command to check if docker or nvidia docker is
    installed
    """
    try:
        ret = subprocess.call([command, ver],
                              stdin=DEVNULL,
                              stdout=DEVNULL,
                              stderr=DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("error: %s must be installed prior " % command,
              "to using the imagepypelines-gpu shell")
        print("for installation help:",
              " https://github.com/NVIDIA/nvidia-docker")
        sys.exit(1)

################################################################################
def make_ping_pipeline():
    import imagepypelines as ip

    # make a few blocks
    @ip.blockify()
    def block1(I):
        time.sleep(50e-3)
        """adds 1 to I"""
        return I + 1

    @ip.blockify()
    def block2(I, II):
        time.sleep(50e-3)
        """adds 1 to I, adds 3 to II"""
        return I + 1, II + 3

    @ip.blockify()
    def block3(I, II):
        time.sleep(50e-3)
        """adds 10 to I, adds 5 to II"""
        return I + 10, II + 5

    @ip.blockify()
    def block4(I, II, III):
        time.sleep(50e-3)
        """adds I, II, III together"""
        return (I + II + III)


    # build the pipeline
    tasks = {  'A' : ip.Input(0),
                'B' : ip.Input(1),
                'C' : (block1, 'A'),
                ('D','E') : (block2, 'C', 'A'),
                ('F','G') : (block3, 'D', 'B'),
                'H' : (block4, 'A', 'D', 'F'),

            }

    pipeline = ip.Pipeline(tasks, name='TestPipeline')

    return pipeline

################################################################################
#                                 Commands
################################################################################
def shell(parser, args):
    """launches the ImagePypelines Shell container"""
    # TO DO - add nested parsers using parser 'parent' argument
    # action == 'shell' | subcommand options
    parser.add_argument('--display',
                        default=':0',
                        help="overload the display variable for X11 access")
    parser.add_argument('-v', '--volume',
                        action='append',
                        default=[])
    parser.add_argument('--gpu',
                        help='launch a container that attempts to access the gpu',
                        action='store_true')
    parser.add_argument('--nest',
                        help='force launching nested containers within containers',
                        action='store_true')
    parser.add_argument('--supress-welcome',
                        help='supress the welcome message',
                        action='store_true')

    args = parser.parse_args()

    image = TAGS[args.gpu]

    if args.gpu:
        # check if nvidia-docker is installed if we are launching GPU image
        command, ver = "nvidia-docker", "version"
        check_docker(command,ver)
    else:
        # check if docker is installed if we are running a cpu image
        command, ver = "docker","--version"
        check_docker(command,ver)

    # check if the variable "IP_ABORT_NESTED_SHELLS" is True to prevent
    # launching ip environments inside ip environments. this can be disabled
    # by the user if they wish
    if "IP_ABORT_NESTED_SHELLS" in os.environ:
        if args.nested:
            should_launch = True
        else:
            should_launch = not (os.environ["IP_ABORT_NESTED_SHELLS"].upper() in [
                                 "YES", "1", "TRUE", "ON"])

    else:
        should_launch = True

    if should_launch == False:
        print("error: canceling shell launch to avoid nested environments")
        print("to force nested environments, you can set the environmental"
              + "variable IP_ABORT_NESTED_SHELLS=OFF")
        sys.exit(1)

    # Docker commands
    # ---- prep the docker command ----
    cmd = [command,
           'run',
           # make interactive
           '-it',
           # set working directory
           '-w', '{0}'.format(POSIX_PATH),
           # set (and remove) limits on hardware resources
           '--security-opt=seccomp:unconfined',
           '--privileged',
           '--net=host',
           '--ulimit', 'rtprio=99:99',
           '--ulimit', 'nice=-20:-20',
           # automatically remove the container
           '--rm',
           # set a recognizable hostname
           '--hostname', HOSTNAMES[args.gpu],
           # X11
           '-e', 'DISPLAY={0}'.format(args.display),
           '-e', 'QT_X11_NO_MITSHM=1',
           # '-e', 'XAUTHORITY=/tmp/.docker.xauth',
           '-e', 'force_color_prompt=1',
           '-e', 'IP_TOOLS_VERSION={}'.format(__version__),
           '-e', 'IP_SUPRESS_WELCOME={}'.format('ON' if args.supress_welcome else 'OFF'),
           ]
    # add default and user-defined volumes to the path
    volumes = DEFAULT_VOLUMES + args.volume
    for path in volumes:
        cmd.extend(['-v', path])

    # add environmental variable containing all the mounted paths
    cmd.extend(['-e', 'MOUNTED_VOLUMES={}'.format(''.join(["  {}\n".format(v) for v in volumes]))])

    # append the image name to the command
    cmd.append(image)
    cmd.append("bash")

    # launch the shell
    print("launching docker image: {}".format(image))
    subprocess.call(cmd)

################################################################################
def build(parser, args):
    """builds the docker images"""
    # add more options and reparse the args
    parser.add_argument('--no-cache',
                        help='rebuilds the docker images without a cache',
                        action='store_true')

    args = parser.parse_args()



    # check if docker is installed
    check_docker('docker','--version')

    for tag, up_tag, dockerfile in zip(TAGS, UPDATE_TAGS, DOCKERFILES):
        cmd = ['docker',
                'build',
                '--pull',
                '--tag',tag,
                '--tag',up_tag,
                '-f',dockerfile,
                BUILD_DIR,
                ]
        if args.no_cache:
            cmd.append('--no-cache')
        subprocess.call(cmd)

################################################################################
def pull(parser, args):
    """pulls the most recent docker images down"""
    # check if docker is installed
    check_docker('docker','--version')
    for tag in TAGS:
        cmd = ['docker',
                'pull',
                tag
                ]

        subprocess.call(cmd)

################################################################################
def push(parser, args):
    """pushes the docker images to dockerhub - DEVS ONLY"""
    print("Warning: \"push\" is only for imagepypelines developers")
    print("Warning: You must be manually logged into docker for this to complete successfully")
    # check if docker is installed
    check_docker('docker','--version')

    # check if the tags we are pushing already exist on the repo
    # this is a little non-intuitive, but basically this fetches
    # a json string that convienently can be evaled into a python list
    # that contains all the tags we have on our repo
    response = urllib.request.urlopen(REGISTRY_URL).read().decode('utf-8')
    remote_tags = [tag['name'] for tag in eval(response,{},{})]
    local_tags = [t.split(':')[1] for t in TAGS]

    # loop through all tags
    for full_tag, local in zip(TAGS, local_tags):
        # if this tags exists remotely, then we abort the push
        if local in remote_tags:
            print("error: {} exists remotely, skipping push!".format(local))
        else:
            print("attempting to push image {}".format(full_tag))
            subprocess.call(["docker", "push", full_tag])

################################################################################
def dashboard(parser, args):
    """launches the dashboard"""
    subprocess.call([sys.executable, FLASK_APP])

################################################################################
def ping(parser, args):
    """spins up a test pipeline to communicate to the given dashboard"""
    parser.add_argument("host",
                        help="IP address of the dashboard server to ping",
                        type=str)
    parser.add_argument("port",
                        help="port number of the dashboard",
                        type=int)
    parser.add_argument("-i", "--interval",
                        help="interval in milliseconds to ping the dashboard",
                        default=1000,
                        type=int)
    parser.add_argument("--no-repeat",
                        help="flag whether or not to repeat this ping",
                        action="store_true")
    args = parser.parse_args()


    # import imagepypelines in a try-catch for verbose
    try:
        import imagepypelines as ip
        ip.set_log_level(100)
    except ImportError:
        print("unable to import ImagePypelines - it must be installed separately. Try \"pip install imagepypelines\"")
        raise

    # build the pipeline
    pipeline = make_ping_pipeline()

    # build internal helper function to connect to the dash and run the pipeline
    def connect_and_run():
        if ip.n_dashboards() == 0:
            ip.connect_to_dash('test_dash', args.host, args.port)
            # print message if we connect or fail to connect
            if ip.n_dashboards() == 0:
                if args.no_repeat:
                    msg = f"unable to connect."
                else:
                    msg = f"unable to connect... retrying in {args.interval}ms"
                print(msg)
            else:
                print("connection success!")


        if ip.n_dashboards():
            print("pinging...")
            pipeline.process(list(range(10)), list(range(10)) )
            time.sleep(args.interval / 1000)


    # connect
    if args.no_repeat:
        connect_and_run()
    else:
        while True:
            connect_and_run()

################################################################################
# ENTRY POINT
def main():
    # parsing command line arguments
    parser = argparse.ArgumentParser(prog='imagepypelines',
                                        usage=__doc__)

    # primary argument
    parser.add_argument('action',
                        help="the primary action to perform",
                        # define acceptable commands
                        choices=["shell",
                                    "push",
                                    "pull",
                                    "build",
                                    "dashboard",
                                    'ping',
                                    ]
                        )

    args = parser.parse_known_args()[0]

    ############################################################################
    # SHELL action --> launch docker container for running imagepypelines apps
    if args.action == "shell":
        shell(parser, args)

    ############################################################################
    elif args.action == "build":
        build(parser, args)

    ############################################################################
    elif args.action == "pull":
        pull(parser, args)

    ############################################################################
    elif args.action == "push":
        push(parser, args)

    ############################################################################
    elif args.action == "dashboard":
        dashboard(parser, args)

    ############################################################################
    elif args.action == "ping":
        ping(parser, args)


if __name__ == "__main__":
    main()

# END
