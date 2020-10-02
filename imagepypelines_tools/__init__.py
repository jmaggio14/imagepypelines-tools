import pkg_resources
DOCKERFILE = pkg_resources.resource_filename(__name__, './dockerfiles/dashboard.Dockerfile')
BUILD_DIR = pkg_resources.resource_filename(__name__, '.')
del pkg_resources

from .version_info import *

DASHBOARD_LATEST_TAG = 'imagepypelines/imagepypelines-tools:latest'
# this tags the dashboard version to this version of iptools if it's built
DASHBOARD_VERSION_TAG = f"dashboard-{__version__}"

from .cli import main
