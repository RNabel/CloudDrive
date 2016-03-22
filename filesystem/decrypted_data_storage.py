"""
Cache files, and evict if maximum storage capacity would be trespassed.
"""
import filesystem
from control.constants import ENCRYPTED_FOLDER_PATH, DECRYPTED_FOLDER_PATH

class DecryptedDataStorage:
    def __init__(self, encrypted_folder=ENCRYPTED_FOLDER_PATH, decrypted_folder=DECRYPTED_FOLDER_PATH):
        self.cache = filesystem.LRUCache(filesystem.CACHE_CAPACITY)

    # Accessor methods.
    def add_file(self, gdrive_file):
        # TODO delete files until desired file size reached, including new object.
        pass

    def retrieve_file(self, id):
        pass
