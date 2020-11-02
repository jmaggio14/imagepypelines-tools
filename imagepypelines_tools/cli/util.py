import subprocess
from subprocess import DEVNULL
import sys
import urllib.request
import time

REGISTRY_URL = "https://registry.hub.docker.com/v1/repositories/imagepypelines/dashboard/tags"

__all__ = ['check_docker',
            'make_ping_pipeline',
            'check_if_tag_exists_on_dockerhub']
################################################################################
def check_docker():
    """runs a system command to check if docker or nvidia docker is
    installed
    """
    try:
        ret = subprocess.call(['docker', '--version'],
                              stdin=DEVNULL,
                              stdout=DEVNULL,
                              stderr=DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Docker must be installed prior to using an containerized tool within ImagePypelines")
        sys.exit(1)


################################################################################
def make_ping_pipeline():
    import imagepypelines as ip
    import time

    # make a few blocks
    @ip.blockify()
    def block1(I):
        """adds 1 to I"""
        time.sleep(50e-3)
        return I + 1

    @ip.blockify()
    def block2(I, II):
        """adds 1 to I, adds 3 to II"""
        time.sleep(50e-3)
        return I + 1, II + 3

    @ip.blockify()
    def block3(I, II):
        """adds 10 to I, adds 5 to II"""
        time.sleep(50e-3)
        return I + 10, II + 5

    @ip.blockify()
    def block4(I, II, III):
        """adds I, II, III together"""
        time.sleep(50e-3)
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
def check_if_tag_exists_on_dockerhub(tag):
    """checks if the given tag exists on our dockerhub"""
    # check if the tags we are pushing already exist on the repo
    # this is a little non-intuitive, but basically this fetches
    # a json string that convienently can be evaled into a python list
    # that contains all the tags we have on our repo
    response = urllib.request.urlopen(REGISTRY_URL).read().decode('utf-8')
    remote_tags = [tag['name'] for tag in eval(response,{},{})]

    if tag in remote_tags:
        return True
    else:
        return False
