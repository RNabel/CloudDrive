import os
import signal

import sys

import control.constants
import filesystem.fuse_endpoint

# Folders used to store local files.
ENC_FOLDER = "/home/robin/PycharmProjects/CloudDrive/temp_enc_folder"
DEC_FOLDER = "/home/robin/PycharmProjects/CloudDrive/temp_dec_folder"

fuse_object = None


def initialise_fuse(mount_point, content_folder):
    global fuse_object
    # Check if the mount point exists, if not create the folder.
    if not os.path.exists(mount_point):
        os.mkdir(mount_point)

    fuse_object = filesystem.fuse_endpoint.main(mount_point, content_folder)


# Register kill signal handler.
def sig_kill_handler(signal, frame):
    print "Got SIGTERM/SIGINT"
    # Forward instruction to tear down.
    exit_code = fuse_object.tear_down()
    # Provide exit code
    sys.exit(exit_code)


signal.signal(signal.SIGTERM, sig_kill_handler)
signal.signal(signal.SIGINT, sig_kill_handler)
signal.signal(signal.SIGUSR1, sig_kill_handler)
signal.signal(signal.SIGUSR2, sig_kill_handler)
signal.signal(signal.SIGQUIT, sig_kill_handler)
signal.signal(signal.SIGALRM, sig_kill_handler)

if __name__ == "__main__":
    useCLI = False

    mountpoint = '/cs/scratch/rn30/mnt'
    root = '/cs/home/rn30/Downloads'
    try:
        initialise_fuse(mountpoint, root)
    except (KeyboardInterrupt, SystemExit):
        print "Oops"
        sig_kill_handler(None, None)

    # Clean up on shut-down.
    sig_kill_handler(None, None)
