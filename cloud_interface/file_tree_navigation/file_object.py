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