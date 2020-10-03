import pkg_resources, os
DOCKERFILE = pkg_resources.resource_filename(__name__, 'dockerfiles/dashboard.Dockerfile')
DOCKER_BUILD_CONTEXT = os.path.abspath(pkg_resources.resource_filename(__name__, '.'))
del pkg_resources, os

from .version_info import *

DASHBOARD_LATEST_TAG = 'imagepypelines/dashboard:latest'
# this tags the dashboard version to this version of iptools if it's built
DASHBOARD_VERSION_TAG = f"imagepypelines/dashboard:{__version__}"

from .cli import main
