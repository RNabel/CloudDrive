import os
import control.constants as constants


class Downloader:
    def __init__(self):
        pass

    def download_file(self, path, file_tree_navigator, fh_id, flags):
        curr_el = file_tree_navigator.navigate(path).get_current_element()

        cached_file_path = constants.DECRYPTED_FOLDER_PATH + constants.FILE_PATH_SEPARATOR + str(curr_el.get_id())

        if not os.path.exists(cached_file_path):
            # Download file.
            curr_el.download_to(cached_file_path)
            os.chmod(cached_file_path, 0o777)

        return os.open(cached_file_path, flags)
