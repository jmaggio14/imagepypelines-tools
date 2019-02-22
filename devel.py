#!/usr/bin/env python3

import argparse
import os
import subprocess

HOME = os.path.expanduser('~')
CURRENT_DIR = os.path.abspath( os.path.dirname(__file__) )


parser = argparse.ArgumentParser()
parser.add_argument('--image',default='devel')
parser.add_argument('--display',default=':0')
parser.add_argument('--xauth',default='/tmp/.docker.xauth')

args = parser.parse_args()


subprocess.run('touch {}'.format(args.xauth), shell=True)
subprocess.run('xauth nlist {} | sed -e \'s/^..../ffff/\' | xauth -f {} nmerge -'.format(args.display, args.xauth),
               shell=True)

CMD = ['nvidia-docker',
         'run',
         # make interactive
         '-it',
         # mount the current directory
         '-v', '{0}:{0}'.format(CURRENT_DIR),
         '-w', '{0}'.format(CURRENT_DIR),
         # set (and remove) limits on hardware resources
        '--security-opt=seccomp:unconfined',
        '--privileged',
        '--net=host',
        '--ulimit', 'rtprio=99:99',
        '--ulimit', 'nice=-20:-20',
        # clion setup
        '-v', '{0}/.CLion2018.3:{0}/.CLion2018.3'.format(HOME),
        '-v', '{0}/Documents/installed/clion-2018.3.4:{0}/Documents/installed/clion-2018.3.4'.format(HOME),
        '-v', '{0}/.java:{0}/.java'.format(HOME),
        '-v', '{0}/.java:{0}/.java'.format(HOME),
        '-v', '{0}/.config:{0}/.config'.format(HOME),
        # graphics and device accesss
        '-v', '/tmp/.X11-unix:/tmp/.X11-unix',
        '-v', '/run/dbus:/run/dbus',
        '-v', '/dev:/dev',
        '-e', 'DISPLAY=:0',
        '-e', 'QT_X11_NO_MITSHM=1',
        '-e', 'XAUTHORITY=/tmp/.docker.xauth',
        '-e', 'HOST_HOME={0}'.format(HOME),
        args.image
        ]

subprocess.run(CMD)
