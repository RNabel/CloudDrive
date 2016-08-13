import strict_rfc3339

import cloud_interface


class FileObject:
    def __init__(self, gdrive_file=None, file_name=None, parent_id=None, is_folder=False):
        """

        Args:
            gdrive_file: pydrive.files.GoogleDriveFile
        """
        # Verify input parameters.
        if gdrive_file or file_name and parent_id:
            if gdrive_file:
                if gdrive_file == 'root':
                    self.file = {'id': 'root',
                                 'metadata': {
                                     'mimeType': 'application/vnd.google-apps.folder'
                                 }
                                 }
                else:
                    self.file = gdrive_file
            else:
                # Create new GDrive object, and Upload it to fill the ID field.
                params = {
                    "parents": [{"kind": "drive#fileLink",
                                 "id": parent_id}],
                    'title': file_name
                }

                if is_folder:
                    params['mimeType'] = "application/vnd.google-apps.folder"
                    params["parents"] = [{"id": parent_id}]

                new_file = cloud_interface.drive.CreateFile(params)

                new_file.Upload()
                self.file = new_file
        else:
            raise Exception("FileObject called with incorrect parameters.")

        self.gauth = None
        self.drive = None
        self.thread_safe = False

    def get_name(self):
        return self.file['title']

    def rename(self, new_name):
        """
        Only changes the name of the GoogleDriveFile, does not change location.
        Returns:
            None
        """
        self.file['title'] = new_name
        self.file.Upload()

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
            return int(self.file['fileSize'])

    def remove(self):
        self.file.Delete()

    def get_mimetype(self):
        return self.file.metadata['mimeType']

    def _convert_date_to_unix(self, date_string):
        return strict_rfc3339.rfc3339_to_timestamp(date_string)

    def get_mtime(self):
        return self._convert_date_to_unix(self.file['modifiedDate'])

    def get_ctime(self):
        return self._convert_date_to_unix(self.file['createdDate'])

    def download_to(self, path):
        fh = open(path, 'w+')
        fh.close()
        self.file.GetContentFile(path)

    def upload_content(self, path):
        if self.is_file():
            self.file.SetContentFile(path)
            self.file.Upload()
