#!/usr/bin/env python


"""
    Running the imagepypelines shell:
        $ imagepypelines shell
        (GPU)
        $ imagepypelines shell --gpu (nvidia-docker required)
        (additonal volumes)
        $ imagepypelines shell -v /host/path:/mount/path
        (force nested containers)
        $ imagepypelines shell --nest

    Rebuilding the imagepypelines docker images for this version
        $ imagepypelines build
        (no cache)
        $ imagepypelines build --no-cache

    Pulling the imagepypelines docker images from dockerhub
        $ imagepypelines pull

imagepypelines [-h] [--display DISPLAY] [-v VOLUME] [--gpu] [--nest]
                      [--no-cache]
                      {shell,push,pull,check}


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

from .version_info import __version__
from . import BUILD_DIR, DOCKERFILES

WORKING_DIR = os.path.abspath( os.getcwd() )
drive = pathlib.Path(WORKING_DIR).drive


if drive != '':
    POSIX_PATH = WORKING_DIR.replace(drive, '/root').replace(os.sep, '/')
else:
    POSIX_PATH = os.path.join('/root', WORKING_DIR).replace(os.sep, '/')


APP = pkg_resources.resource_filename(__name__, "app.py")

DEFAULT_VOLUMES = ['{0}:{1}'.format(WORKING_DIR, POSIX_PATH)]
BASE_TAGS = ['imagepypelines/imagepypelines-tools:base',
                'imagepypelines/imagepypelines-tools:gpu']
TAGS = [tag + '-%s' % __version__ for tag in BASE_TAGS]
UPDATE_TAGS = ["imagepypelines/imagepypelines-tools:latest",
                "imagepypelines/imagepypelines-tools:latest-gpu"]
HOSTNAMES = ['imagepypelines', 'imagepypelines-gpu']
REGISTRY_URL = "https://registry.hub.docker.com/v1/repositories/imagepypelines/imagepypelines-tools/tags"

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
                                    "check",
                                    "monitor",
                                    ]
                        )

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

    # action == 'build' | subcommand options
    parser.add_argument('--no-cache',
                        help='rebuilds the docker images without a cache',
                        action='store_true')

    args = parser.parse_args()

    # SHELL action --> launch docker container for running imagepypelines apps
    if args.action == "shell":
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

    elif args.action == "check":
        # check to see if all imagepypelines dependencies are installed
        print("this feature is temporarily disabled")
        # requirements = {'setuptools': '39.0.0',
        #                 'PIL': '4.0',
        #                 'colorama': '0.4.0',
        #                 'keras': '2.2.4',
        #                 'numpy': '1.14',
        #                 'sklearn': '0.20.0',
        #                 'scipy': '1.1.0',
        #                 'termcolor': '1.0',
        #                 'tensorflow': '1.12.0',
        #                 'cv2': '3.4.0',
        #                 }
        # bad_packages = set()
        #
        # for req, version in requirements.items():
        #     # see if package is importable
        #     try:
        #         package = importlib.import_module(req)
        #
        #     except ImportError:
        #         print("unable to import {}".format(req))
        #         bad_packages.add(req)
        #
        #     # check version of package
        #     if version > package.__version__:
        #         print("({}) requires version {}, but you have {}".format(
        #             req, version, package.__version__))
        #         bad_packages.add(req)
        #
        #     # print success of failure
        # if len(bad_packages) == 0:  # success
        #     print("all package dependencies are met")
        #     sys.exit(0)
        # else:  # failure
        #     print("package dependencies not met")
        #     sys.exit(1)
    elif args.action == "build":
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

    elif args.action == "pull":
        # check if docker is installed
        check_docker('docker','--version')
        for tag in TAGS:
            cmd = ['docker',
                    'pull',
                    tag
                    ]

            subprocess.call(cmd)


    elif args.action == "push":
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

    elif args.action == "monitor":
        subprocess.call([sys.executable, os.path.join(APP)])


    """
    *within a shell*
    imagepypelines <action>
    """

if __name__ == "__main__":
    main()

# END
