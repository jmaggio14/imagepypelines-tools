from . import DASHBOARD_LATEST_TAG
from . import DASHBOARD_VERSION_TAG

def push(parser, args):
    """pushes the docker images to dockerhub - DEVS ONLY"""
    print("Warning: \"push\" is only for imagepypelines developers")
    print("Warning: You must be manually logged into docker for this to complete successfully")
    # check if docker is installed
    check_docker()

    # push the latest tag no matter what
    print(f"attempting to push image {DASHBOARD_LATEST_TAG}")
    subprocess.run(["docker", "push", DASHBOARD_LATEST_TAG])

    # NOTE: should we change to push the version tag
    # only if it doesn't already exist on dockerhub? -JM
    print(f"attempting to push image {DASHBOARD_VERSION_TAG}")
    subprocess.run(["docker", "push", DASHBOARD_VERSION_TAG])
