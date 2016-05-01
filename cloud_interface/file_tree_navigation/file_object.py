import datetime
import strict_rfc3339
from cloud_interface.file_tree_navigation import structure_fetcher as sf
import cloud_interface


class FileObject:
    def __init__(self, gdriveFile=None, file_name=None, parent_id=None, is_folder=False):
        """

        Args:
            gdriveFile: pydrive.files.GoogleDriveFile
        """
        # Verify input parameters.
        if gdriveFile or file_name and parent_id:
            if gdriveFile:
                if gdriveFile == 'root':
                    self.file = {'id': 'root',
                                 'metadata': {
                                     'mimeType': 'application/vnd.google-apps.folder'
                                 }
                                 }
                else:
                    self.file = gdriveFile
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

    def remove(self):
        file_id = self.get_id()
        self.file.DeleteFile(file_id)

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
        sf.drive.CreateFile({'id': self.get_id()}).GetContentFile(path)

    def upload_content(self, path):
        if self.is_file():
            drive_file = sf.drive.CreateFile({
                'id': self.get_id(),
                'mimeType': self.get_mimetype()
            })
            drive_file.SetContentFile(path)

            drive_file.Upload()
