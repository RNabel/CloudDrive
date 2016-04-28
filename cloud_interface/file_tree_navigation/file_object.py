import datetime
from cloud_interface.file_tree_navigation import structure_fetcher as sf


class FileObject:
    def __init__(self, gdriveFile):
        """

        Args:
            gdriveFile: pydrive.files.GoogleDriveFile
        """
        self.file = gdriveFile

    def get_name(self):
        return self.file['title']

    def is_folder(self):
        return self.file.metadata['mimeType'] == 'application/vnd.google-apps.folder'

    def is_file(self):
        return 'application/vnd.google-apps' not in self.file.metadata['mimeType']

    def get_id(self):
        return self.file['id']

    def get_size(self):
        if self.is_folder():
            return 10  # TODO return number of entries
        else:
            return int(self.file['quotaBytesUsed'])

    def _convert_date_to_unix(self, date_string):
        dt = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        return (dt - datetime.datetime(1970, 1, 1)).total_seconds()

    def get_mtime(self):
        return self._convert_date_to_unix(self.file['modifiedDate'])

    def get_ctime(self):
        return self._convert_date_to_unix(self.file['createdDate'])

    def download_to(self, path):
        fh = open(path, 'w+')
        fh.close()
        sf.drive.CreateFile({'id': self.get_id()}).GetContentFile(path)
