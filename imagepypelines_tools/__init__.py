from .version_info import *

import pkg_resources

GENERAL_DASHBOARD_TAG = 'imagepypelines/imagepypelines-tools:latest'
# this tags the dashboard version to this version of iptools if it's built
VERSION_DASHBOARD_TAG = f"dashboard-{__version__}"

BUILD_DIR = pkg_resources.resource_filename(__name__, '../dockerfiles')
DOCKERFILE = pkg_resources.resource_filename(__name__,
                                            'dockerfiles/dashboard.Dockerfile')

del pkg_resources

from .cli import main
