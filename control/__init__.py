import os
import signal
import sys

import control.constants
import filesystem.fuse_endpoint
import secrets
from control import tools

fuse_object = None
logger = None

def initialise_fuse(_mount_point, _temp_storage):
    global fuse_object
    # Check if the mount point exists, if not create the folder.
    if not os.path.exists(_mount_point):
        os.mkdir(_mount_point)

    fuse_object = filesystem.fuse_endpoint.main(_mount_point, _temp_storage)


# Tear down method.
def tear_down(_signal=None, frame=None):
    logger.info("Got SIGTERM/SIGINT")
    # Forward instruction to tear down.
    exit_code = fuse_object.tear_down()

    logger.info("Tear-down done, exiting.")
    # Provide exit code
    sys.exit(exit_code)

# These are not working since fusepy runs a C-level loop, which can not be interrupted with Python-level interrupts.
# Event handlers in action while fuse not running, so setup can be used in future iterations.
signal.signal(signal.SIGTERM, tear_down)
signal.signal(signal.SIGINT, tear_down)
signal.signal(signal.SIGUSR1, tear_down)
signal.signal(signal.SIGUSR2, tear_down)
signal.signal(signal.SIGQUIT, tear_down)
signal.signal(signal.SIGALRM, tear_down)

if __name__ == "__main__":
    logger = tools.setup_logger("ControlLogger")

    # Set the mount point and temporary storage location. TODO move into a settings context.
    mount_point = secrets.MOUNT_POINT
    temp_storage = secrets.TEMP_STORAGE

    # This function will not return until the process receives a SIGINT or SIGKILL interrupt.
    initialise_fuse(mount_point, temp_storage)

    # Clean up on shut-down.
    tear_down()
