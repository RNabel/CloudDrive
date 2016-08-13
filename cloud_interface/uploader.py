import control.constants as constants


class Uploader:
    def __init__(self):
        pass

    def upload_file(self, file_obj):
        cached_file_path = constants.DECRYPTED_FOLDER_PATH + constants.FILE_PATH_SEPARATOR + str(file_obj.get_id())
        file_obj.upload_content(cached_file_path)
