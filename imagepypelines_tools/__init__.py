import pkg_resources
DOCKERFILES = [pkg_resources.resource_filename(__name__,
                        'dockerfiles/dashboard.Dockerfile'),
                ]
BUILD_DIR = pkg_resources.resource_filename(__name__, 'dockerfiles')

TEMPLATES_DIR = pkg_resources.resource_filename(__name__, 'templates')
LAYOUTS_DIR = pkg_resources.resource_filename(__name__, 'templates/layouts')

del pkg_resources
from .version_info import *
from .imagepypelines_tools import main
