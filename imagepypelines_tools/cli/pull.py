import subprocess
from .util import check_docker, check_if_tag_exists_on_dockerhub

from .. import GENERAL_DASHBOARD_TAG, VERSION_DASHBOARD_TAG


def pull(parser, args):
    """pulls the most recent docker images down"""
    # check if docker is installed
    check_docker()
    cmd = ['docker',
            'pull',
            GENERAL_DASHBOARD_TAG,
            ]


    if check_if_tag_exists_on_dockerhub(VERSION_DASHBOARD_TAG):
        cmd.append(VERSION_DASHBOARD_TAG)

    subprocess.run(cmd)
