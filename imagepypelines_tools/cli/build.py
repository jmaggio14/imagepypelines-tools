import subprocess
from .util import check_docker

from . import DOCKERFILE
from . import BUILD_DIR
from . import DASHBOARD_LATEST_TAG
from . import DASHBOARD_VERSION_TAG



def build(parser, args):
    """builds the dashboard image"""
    # add more options and reparse the args
    parser.add_argument('--no-cache',
                        help='rebuilds the docker images without using the layer cache',
                        action='store_true')

    args = parser.parse_args()

    # check if docker is installed
    check_docker()

    cmd = ['docker',
            'build',
            '--pull',
            '--tag',DASHBOARD_LATEST_TAG,
            '--tag',DASHBOARD_VERSION_TAG,
            '-f',DOCKERFILE,
            BUILD_DIR,
            ]
    if args.no_cache:
        cmd.append('--no-cache')
    subprocess.run(cmd)
