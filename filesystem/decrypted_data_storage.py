"""
Cache files, and evict if maximum storage capacity would be trespassed.
"""
import os
import filesystem
from control.constants import ENCRYPTED_FOLDER_PATH, DECRYPTED_FOLDER_PATH, FILE_PATH_SEPARATOR


class DecryptedDataStorage:
    def __init__(self, encrypted_folder_path=ENCRYPTED_FOLDER_PATH, decrypted_folder_path=DECRYPTED_FOLDER_PATH):
        self.cache = filesystem.LRUCache(filesystem.CACHE_CAPACITY)
        self.encrypted_folder_path = encrypted_folder_path
        self.decrypted_folder_path = decrypted_folder_path

    # Accessor methods.
    def open_file(self, file_obj, flags):
        """
        Open the file with specified flags, download if necessary, associate caching state object.
        Args:
            file_obj: file_tree_navigation.file_object.FileObject representing the file to be opened.
            flags: the flags to pass to the os.open call.

        Returns:
            os file pointer, cache state
        """
        cached_file_path = self.decrypted_folder_path + FILE_PATH_SEPARATOR + str(file_obj.get_id())

        if not os.path.exists(cached_file_path):
            # Download file.
            file_obj.download_to(cached_file_path)
            os.chmod(cached_file_path, 0o777)

        os_fptr = os.open(cached_file_path, flags)

        return os_fptr, None

    def create_file(self, file_obj, mode, flags):
        cached_file_path = self.decrypted_folder_path + FILE_PATH_SEPARATOR + str(file_obj.get_id())
        os_fptr = os.open(cached_file_path, flags, mode)

        return os_fptr, None

    # Getters and setters
    # ===================
    def get_encrypted_folder(self):
        return self.encrypted_folder_path

    def get_decrypted_folder(self):
        return self.decrypted_folder_path
