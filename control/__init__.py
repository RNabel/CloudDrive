import filesystem.fuse_endpoint
import os

# Folders used as to store local files.
ENC_FOLDER = "/home/robin/PycharmProjects/CloudDrive/temp_enc_folder"
DEC_FOLDER = "/home/robin/PycharmProjects/CloudDrive/temp_dec_folder"


def initialise_fuse(mount_point, content_folder):
    # Check if the mount point exists, if not create the folder.
    if not os.path.exists(mount_point):
        os.mkdir(mount_point)

    filesystem.fuse_endpoint.main(mount_point, content_folder)


if __name__ == "__main__":
    # test start the fuse system.
    initialise_fuse("/home/robin/fuse_mount", "/home/robin/fuse_content")
