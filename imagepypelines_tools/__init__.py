from .version_info import *

import pkg_resources

DASHBOARD_LATEST_TAG = 'imagepypelines/imagepypelines-tools:latest'
# this tags the dashboard version to this version of iptools if it's built
DASHBOARD_VERSION_TAG = f"dashboard-{__version__}"

BUILD_DIR = pkg_resources.resource_filename(__name__, '../dockerfiles')
DOCKERFILE = pkg_resources.resource_filename(__name__,
                                            'dockerfiles/dashboard.Dockerfile')

del pkg_resources

from .cli import main
