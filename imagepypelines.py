#!/usr/bin/env python3

import argparse
import os
import subprocess

HOME = os.path.expanduser('~')
CURRENT_DIR = os.path.abspath( os.path.dirname(__file__) )
POSIX_PATH = CURRENT_DIR.replace(HOME,'/root').replace(os.sep,'/')


parser = argparse.ArgumentParser()
parser.add_argument('--image',default='imagepypelines')
parser.add_argument('--display',default=':0')

args = parser.parse_args()

# subprocess.run('touch {}'.format(args.xauth), shell=True)
# subprocess.run('xauth nlist {} | sed -e \'s/^..../ffff/\' | xauth -f {} nmerge -'.format(args.display, args.xauth),
#                shell=True)

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
        args.image
        ]

subprocess.call(CMD)
# subprocess.run(CMD)
