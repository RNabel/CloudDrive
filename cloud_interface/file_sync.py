# Code to upload and download files from Google Drive.
import os
from cloud_interface import drive
from control import ENC_FOLDER
from filesystem import file_cache
import encryption


def sync_file(path, remote_target, encrypt=True):
    """
    Synchronize state of file between local storage and remote storage.
    Args:
        encrypt: Whether to encrypt file before upload.
        remote_target: The unique id assigned by remote storage and also used by local storage.
        path: The local file path.

    Returns:
        integer: 0 if successful, 1 otherwise.
    """
    # Encrypt file as necessary.
    if encrypt:
        path = encryption.encrypt_file(path)
    _upload_file(path, remote_target)


# Helpers.
# TODO may have to ensure this is done atomically.
# TODO What happens if it is a new file?
def _upload_file(content_file_path, parent_id):
    """
    Upload file to remote storage.
    Args:
        content_file_path: The unique id used locally and on remote to identify file.
        parent_id: The id assigned to the parent folder.
    Returns:
        integer: success code.
    """
    file_name = os.path.basename(content_file_path)

    up_file = drive.CreateFile({
        'description': 'An excellent file you will find to be to your liking.',
        "parents": [{"kind": "drive#fileLink",
                     "id": parent_id}],
        'title': file_name
    })
    up_file.SetContentFile(content_file_path)
    up_file.Upload()


def create_folder(folder_name, parent_id):
    """
    Create new folder object and upload it to GDrive.
    Args:
        folder_name: The title/name of the folder.
        parent_id: The id of the parent folder.

    Returns: None
    """
    folder = drive.CreateFile({'title': folder_name,
                               "parents": [{"id": parent_id}],
                               "mimeType": "application/vnd.google-apps.folder"})
    folder.Upload()


def _delete_file(file_id):
    file_obj = drive.CreateFile({'id': file_id})
    file_obj.DeleteFile(file_id)


def _download_file(file_id):
    """
    Download file from remote storage.
    Args:
        file_id: The unique id used locally and on remote to identify file.

    Returns:
        integer: success code, 0 if success, 1 otherwise.
    """
    file_obj = drive.CreateFile({'id': file_id})

    # Add reference about size etc. to cache.
    # TODO need to get file size BEFORE downloading it.
    file_cache.set_file(file_obj)

    # Download content of file.
    file_obj.GetContentFile(ENC_FOLDER + "/" + file_id)


def _fetch_file_info(file_id):
    """
    Download metadata of one file from the remote.
    Args:
        file_id: The unique id of the file assigned by remote storage.

    Returns:
        GoogleDriveFile with the metadata.
    """
    pass


def _fetch_all_file_info(parent, time=None):
    """
    Download metadata of all files which were changed since specified time.
    Args:
        parent: The id of the parent folder
        time: Unix time of last global fetch.

    Returns:
        List of GoogleDriveFile objects with metadata about each file.
    """
    if parent:
        query_string = "'{}' in parents and ".format(parent)
    else:
        query_string = ""

    return drive.ListFile({'q': query_string + "trashed=false"}).GetList()
