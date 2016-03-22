import os

from pydrive.files import GoogleDriveFile
from control.constants import FILE_PATH_SEPARATOR as PATH_SEPARATOR, DECRYPTED_FOLDER_PATH, ENCRYPTED_FOLDER_PATH


class FileBuffer:
    def __init__(self, storage_folder):
        self.path = storage_folder
        self.files = dict()

    def get_file_path(self, file_id):
        """
        Return the absolute file path of the requested id.
        Args:
            file_id (str):

        Returns:
            Union[str, bool]: The absolute file path if file is downloaded, False otherwise.
        """
        if file_id in self.files:
            return self._create_file_name(self.files[file_id])
        else:
            return False

    def add_file(self, file_obj, gdrive_file):
        """
        Add the specified file to the buffer. Copy the passed in file object, and then delete it.
        Args:
            file_obj (file): The file to copy into the buffer.
            gdrive_file (GoogleDriveFile): The GDrive file to add.

        Returns:
            bool: Whether adding was successful.
        """
        file_path = file_obj.name
        new_file_path = self._create_file_name(gdrive_file)

        # Copy the file.
        os.rename(file_path, new_file_path)

    def remove_file(self, file_id):
        pass

    def _create_file_name(self, gdrive_file):
        file_id = gdrive_file["id"]
        file_name = self.path + PATH_SEPARATOR + file_id

        return file_name


class EncryptedFileBuffer(object, FileBuffer):
    def __init__(self, storage_folder=ENCRYPTED_FOLDER_PATH):
        super(EncryptedFileBuffer, self).__init__(storage_folder)

    def download_file(self, gdrive_file):
        """
        Downloads a google drive file from the internet.
        Args:
            gdrive_file (GoogleDriveFile): The file to download.

        Returns:

        """
        file_id = gdrive_file["id"]
        self.files[file_id] = gdrive_file

        file_path = self._create_file_name(gdrive_file)
        gdrive_file.GetContentFile(file_path)

    def upload_file(self, gdrive_file):
        """
        Upload the specified gdrive_file
        Args:
            gdrive_file (GoogleDriveFile): The file to upload.

        Returns:

        """

    def remove_file(self, file_id):
        file_path = self.get_file_path(file_id)

        if file_path:
            return open(file_path, "w+")
        else:
            return False


class DecryptedFileBuffer(object, FileBuffer):
    def __init__(self, storage_folder=DECRYPTED_FOLDER_PATH):
        super(DecryptedFileBuffer, self).__init__(storage_folder)
    # TODO finish this part.
