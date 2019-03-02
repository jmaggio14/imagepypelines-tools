#!/usr/bin/env python

import argparse
import os
import subprocess
from subprocess import DEVNULL
import importlib
import sys

HOME = os.path.expanduser('~')
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
POSIX_PATH = CURRENT_DIR.replace(HOME, '/root').replace(os.sep, '/')
DEFAULT_VOLUMES = ['{0}:{1}'.format(CURRENT_DIR, POSIX_PATH)]

WELCOME_MSG_TEMPLATE = """
Welcome to the imagepypelines virtual container!

This docker image contains all dependencies you need to run vanilla imagepypelines apps. The source for this dockerfile can be found here: https://github.com/jmaggio14/imagepypelines-tools/blob/master/imagepypelines-base/dockerfile

the following folders have been mounted to this container:
{}

you can mount additional folders with the following
	imagepypelines shell -v /path/to/folder/on/host:/where/you/want/to/mount/it

some things to note:
	> as of now, graphics are not supported in this container
	> any changes made to folders not listed above will NOT be persistent
	> you are root. so no need to use sudo :p
"""

def main():
	# parsing command line arguments
	parser = argparse.ArgumentParser()

	# primary argument
	parser.add_argument('action', help="""
	shell : to enter the imagepypelines docker container
	check : to check if all imagepypelines dependencies are installed
	"""
	                    )
	# action == 'shell' | subcommand options
	parser.add_argument('--image-overload',
	                    default='jmaggio14/imagepypelines:base',
	                    # default='jmaggio14/imagepypelines',
	                    help="the name of the docker image you wish to run instead of the default")
	parser.add_argument('--display',
	                    default=':0',
	                    help="overload the display variable for X11 access")
	parser.add_argument('-v', '--volume',
	                    action='append',
	                    default=[])

	args = parser.parse_args()


	# SHELL action --> launch docker container for running imagepypelines apps
	if args.action == "shell":
	    # TODO check if docker is installed
		try:
			ret = subprocess.call('docker --version',
				stdin=DEVNULL,
				stdout=DEVNULL,
				stderr=DEVNULL)
		except (subprocess.CalledProcessError, FileNotFoundError):
			print("error: docker must be installed prior to using the imagepypelines shell")
			print("for installation help: https://docs.docker.com/install/")
			exit(1)

	    # ---- prep the docker command ----
		CMD = ['docker',
	           'run',
	           # make interactive
	           '-it',\
	           # set working directory
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
	           '-e', 'force_color_prompt=1',
	           ]
	    # add default and user-defined volumes to the path
		volumes = DEFAULT_VOLUMES + args.volume
		for path in volumes:
		    CMD.extend(['-v', path])
		# add environmental variable containing all the mounted paths
		CMD.extend(['-e', 'MOUNTED_VOLUMES={}'.format("|".join(volumes))])
		welcome_msg = WELCOME_MSG_TEMPLATE.format(''.join(["  {}\n".format(v) for v in volumes]))
		CMD.extend(['-e', 'WELCOME_MSG="{}"'.format(welcome_msg)])

		# append the image name to the command
		CMD.append(args.image_overload)
		CMD.append("bash")

	    # launch the shell
		subprocess.call(CMD)

	elif args.action == "check":
	    # check to see if all imagepypelines dependencies are installed
	    requirements = {'setuptools': '39.0.0',
	                    'PIL': '4.0',
	                    'colorama': '0.4.0',
	                    'keras': '2.2.4',
	                    'numpy': '1.14',
	                    'sklearn': '0.20.0',
	                    'scipy': '1.1.0',
	                    'termcolor': '1.0',
	                    'tensorflow': '1.12.0',
	                    'cv2': '3.4.0',
	                    }
	    bad_packages = set()

	    for req, version in requirements.items():
	        # see if package is importable
	        try:
	            package = importlib.import_module(req)

	        except ImportError:
	            print("unable to import {}".format(req))
	            bad_packages.add(req)

	        # check version of package
	        if version > package.__version__:
	            print("({}) requires version {}, but you have {}".format(
	                req, version, package.__version__))
	            bad_packages.add(req)

	        # print success of failure
	        if len(bad_packages) == 0:  # success
	            print("all package dependencies are met")
	            sys.exit(0)
	        else:  # failure
	            print("package dependencies not met")
	            sys.exit(1)

if __name__ == "__main__":
	main()

# END