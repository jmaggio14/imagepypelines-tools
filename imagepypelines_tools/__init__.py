from pkg_resources import resource_filename

GENERAL_DASHBOARD_TAG = 'imagepypelines/imagepypelines-tools:dashboard'
# this tags the dashboard version to this version of iptools if it's built
VERSION_DASHBOARD_TAG = f"{GENERAL_DASHBOARD_TAG}-{__version__}"

DOCKERFILE = resource_filename(__name__, 'dockerfiles/dashboard.Dockerfile')
BUILD_DIR = resource_filename(__name__, 'dockerfiles')


del resource_filename

from .version_info import *
from .imagepypelines_tools import main
