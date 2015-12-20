# Code to upload and download files from Google Drive.
from cloud_interface import drive
from control import ENC_FOLDER
from filesystem import file_cache


def sync_file(id):
    """
    Synchronize state of file between local storage and remote storage.
    Args:
        id: The unique id assigned by remote storage and also used by local storage.

    Returns:
        integer: 0 if successful, 1 otherwise.
    """
    # TODO
    # get metadata
    # compare to newly fetched metadata
    # upload/ download if necessary
    pass


# Helpers.
# TODO may have to ensure this is done atomically.
# TODO What happens if it is a new file?
def _upload_file(id):
    """
    Upload file to remote storage.
    Args:
        id: The unique id used locally and on remote to identify file.

    Returns:
        integer: success code.
    """
    pass


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
    pass
