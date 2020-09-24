from .. import GENERAL_DASHBOARD_TAG
from .. import VERSION_DASHBOARD_TAG

def push(parser, args):
    """pushes the docker images to dockerhub - DEVS ONLY"""
    print("Warning: \"push\" is only for imagepypelines developers")
    print("Warning: You must be manually logged into docker for this to complete successfully")
    # check if docker is installed
    check_docker()

    # loop through all tags
    for tag in [GENERAL_DASHBOARD_TAG, VERSION_DASHBOARD_TAG]:
        # if this tags exists remotely, then we abort the push
        if tag in remote_tags:
            print(f"error: {tag} exists remotely, skipping push!")
        else:
            print(f"attempting to push image {tag}")
            subprocess.run(["docker", "push", tag])
