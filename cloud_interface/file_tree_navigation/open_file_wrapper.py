"""
Wrapper class used for each open file instance. Combines the file_object information with open file handle, and cache
state information.
"""


class OpenFileWrapper:
    def __init__(self, file_obj, file_handle, cache_state):
        self.file_obj = file_obj
        self.file_handle = file_handle
        self.cache_state = cache_state

    def get_file_object(self):
        return self.file_obj

    def get_file_handle(self):
        return self.file_handle

    def get_cache_state(self):
        return self.cache_state
