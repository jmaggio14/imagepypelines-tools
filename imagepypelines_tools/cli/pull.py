import subprocess
from .util import check_docker, check_if_tag_exists_on_dockerhub

from . import DASHBOARD_LATEST_TAG, DASHBOARD_VERSION_TAG


def pull(parser, args):
    """pulls the most recent docker images down"""
    # check if docker is installed
    check_docker()
    cmd = ['docker',
            'pull',
            DASHBOARD_LATEST_TAG,
            ]


    if check_if_tag_exists_on_dockerhub(DASHBOARD_VERSION_TAG):
        cmd.append(DASHBOARD_VERSION_TAG)

    subprocess.run(cmd)
