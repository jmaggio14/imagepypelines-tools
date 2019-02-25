#!/usr/bin/env python3

import argparse
import os
import subprocess

HOME = os.path.expanduser('~')
CURRENT_DIR = os.path.abspath( os.path.dirname(__file__) )
POSIX_PATH = CURRENT_DIR.replace(HOME,'/root').replace(os.sep,'/')

# parsing command line arguments
parser = argparse.ArgumentParser()

# primary argument
parser.add_argument('action')
# action == 'launch' | subcommand options
parser.add_argument('--image-overload',default='imagepypelines')
parser.add_argument('--display',default=':0')

args = parser.parse_args()

# LAUNCH action --> launch docker container for running imagepypelines apps
if args.action == "launch":

    CMD = ['docker',
             'run',
             # make interactive
             '-it',
             # mount the current directory
             '-v', '{0}:{1}'.format(CURRENT_DIR,POSIX_PATH),
             '-w', '{0}'.format(POSIX_PATH),
             # set (and remove) limits on hardware resources
            '--security-opt=seccomp:unconfined',
            '--privileged',
            '--net=host',
            '--ulimit', 'rtprio=99:99',
            '--ulimit', 'nice=-20:-20',
            # X11
            '-e', 'DISPLAY={0}'.format(args.display),
            '-e', 'QT_X11_NO_MITSHM=1',
            # '-e', 'XAUTHORITY=/tmp/.docker.xauth',
            '-e', 'HOST_HOME={0}'.format(HOME),
            '-e','force_color_prompt=1',
            args.image_overload
            ]

    subprocess.call(CMD)
