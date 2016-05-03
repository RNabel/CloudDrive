import os
import signal

import sys

import control.constants
import filesystem.fuse_endpoint

# Folders used to store local files.
ENC_FOLDER = "/home/robin/PycharmProjects/CloudDrive/temp_enc_folder"
DEC_FOLDER = "/home/robin/PycharmProjects/CloudDrive/temp_dec_folder"

fuse_object = None


def initialise_fuse(mount_point, temp_storage):
    global fuse_object
    # Check if the mount point exists, if not create the folder.
    if not os.path.exists(mount_point):
        os.mkdir(mount_point)

    fuse_object = filesystem.fuse_endpoint.main(mount_point, temp_storage)


# Tear down method.
def tear_down(signal=None, frame=None):
    print "Got SIGTERM/SIGINT"
    # Forward instruction to tear down.
    exit_code = fuse_object.tear_down()

    print "Tear-down done, exiting."
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
    useCLI = False
    isCS = True
    if isCS:
        mount_point = '/cs/scratch/rn30/mnt'
        temp_storage = '/cs/scratch/rn30/Temp'
    else:
        mount_point = '/home/robin/CloudDrive'
        temp_storage = '/home/robin/Temp'

    # This function will not return until the process receives a SIGINT or SIGKILL interrupt.
    initialise_fuse(mount_point, temp_storage)

    # Clean up on shut-down.
    tear_down()
