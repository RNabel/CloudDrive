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

    def get_id(self):
        return self.file['id']

    def download_to(self, path):
        fh = open(path, 'w+')
        fh.close()
        sf.drive.CreateFile({'id': self.get_id()}).GetContentFile(path)
