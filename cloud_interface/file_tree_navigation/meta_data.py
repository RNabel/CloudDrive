import os
import pickle
import strict_rfc3339

import control
from cloud_interface import drive


class MetaDataWrapper:
    def __init__(self, file_tree):
        self.file_tree = file_tree
        self.last_update = None
        self.fcb_list = None
        self.metadata_storage_path = control.constants.PROJECT_FOLDER + '/meta_data.txt'

        self.first_load = True  # Indicates whether first batch of data had to be downloaded.
        self.dirty = False

    def save(self):
        # Saves file tree and last update.
        if self.dirty or self.first_load:
            pickle_obj = self._create_pickle_obj()
            pickle.dump(pickle_obj, open(self.metadata_storage_path, 'w+'))

    def load(self):
        # Download metadata of all files.
        if os.path.exists(self.metadata_storage_path):
            self.first_load = False
            pickled_obj = pickle.load(open(self.metadata_storage_path))
            self._convert_pickle_obj(pickled_obj)
            return True
        else:
            self.set_update_time_to_now()
            self.fcb_list = drive.ListFile({'q': "trashed=false"}).GetList()
            return self.fcb_list

    def update(self):
        pass

    def set_update_time_to_now(self):
        if self.last_update is not None:
            self.dirty = True

        self.last_update = strict_rfc3339.now_to_rfc3339_utcoffset()

    def get_update_time(self):
        return self.last_update

    def _create_pickle_obj(self):
        return {
            'file_tree': self.file_tree,
            'last_update': self.last_update
        }

    def _convert_pickle_obj(self, loaded_obj):
        if 'file_tree' in loaded_obj and 'last_update' in loaded_obj:
            self.file_tree = loaded_obj['file_tree']
            self.last_update = loaded_obj['last_update']
        else:
            raise Exception("MetaDataWrapper loaded incorrectly formatted file.")