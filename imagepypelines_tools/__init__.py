import pkg_resources
DOCKERFILES = [pkg_resources.resource_filename(__name__,
                        'dockerfiles/dashboard.Dockerfile'),
                ]
BUILD_DIR = pkg_resources.resource_filename(__name__, 'dockerfiles')

del pkg_resources
from .version_info import *
from .imagepypelines_tools import main
