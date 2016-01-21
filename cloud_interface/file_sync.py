# Code to upload and download files from Google Drive.
import os
from cloud_interface import drive
from control import ENC_FOLDER
from filesystem import file_cache


def sync_file(path, remote_target):
    """
    Synchronize state of file between local storage and remote storage.
    Args:
        remote_target: The unique id assigned by remote storage and also used by local storage.
        path: The local file path.

    Returns:
        integer: 0 if successful, 1 otherwise.
    """

    _upload_file(path, remote_target)


# Helpers.
# TODO may have to ensure this is done atomically.
# TODO What happens if it is a new file?
def _upload_file(path, remote_target):
    """
    Upload file to remote storage.
    Args:
        _id: The unique id used locally and on remote to identify file.

    Returns:
        integer: success code.
    """
    file_name = os.path.basename(path)

    up_file = drive.CreateFile({
        'description': 'AN excellent file you will find to be to your liking.',
        "parents": [{"kind": "drive#fileLink",
                     "id": '0B46HJMu9Db4xTUxhQ0x4WHpfVmM'}], # target folder id here.
        'title': file_name
    })
    up_file.SetContentFile(path)
    up_file.Upload()


def _download_file(id):
    """
    Download file from remote storage.
    Args:
        id: The unique id used locally and on remote to identify file.

    Returns:
        integer: success code, 0 if success, 1 otherwise.
    """
    file_obj = drive.CreateFile({'id': id})

    # Add reference about size etc. to cache.
    # TODO need to get file size BEFORE downloading it.
    file_cache.set_file(file_obj)

    # Download content of file.
    file_obj.GetContentFile(ENC_FOLDER + "/" + id)


def _fetch_file_info(id):
    """
    Download metadata of one file from the remote.
    Args:
        id: The unique id of the file assigned by remote storage.

    Returns:
        GoogleDriveFile with the metadata.
    """
    pass


def _fetch_all_file_info(time):
    """
    Download metadata of all files which were changed since specified time.
    Args:
        time: Unix time of last global fetch.

    Returns:
        List of GoogleDriveFile objects with metadata about each file.
    """
    return drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
