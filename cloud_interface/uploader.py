import os
import control.constants as constants


class Uploader:
    def __init__(self):
        pass

    def upload_file(self, path, file_tree_navigator, fh):
        curr_el = file_tree_navigator.navigate(path).get_current_element()
        cached_file_path = constants.DECRYPTED_FOLDER_PATH + constants.FILE_PATH_SEPARATOR + str(curr_el.get_id())

        curr_el.upload_content(cached_file_path)
