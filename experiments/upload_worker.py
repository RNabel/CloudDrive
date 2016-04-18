"""
Class which wraps the functionality of an individual upload.
"""
import time

import os

from cloud_interface import gauth
from control import tools


class UploadWorker:
    def __init__(self, index, file_id, filename, total_file_num, parent_folder_id, upload_file_name):
        self.index = index
        self.upload_name = upload_file_name

        # Set up upload params.
        self.params = {'title': self.upload_name,
                       'parents': [{"kind": "drive#fileLink", "id": parent_folder_id}],
                       'mimeType': 'text/csv',
                       'properties': [
                           {"value": (str(file_id)), "key": "CloudDrive_id", "visibility": "PUBLIC"},
                           {"value": (str(index)), "key": "CloudDrive_part", "visibility": "PUBLIC"},
                           {"value": (str(filename)), "key": "CloudDrive_filename", "visibility": "PUBLIC"},
                           {"value": (str(total_file_num)), "key": "CloudDrive_total", "visibility": "PUBLIC"}
                       ]
                       }

        # Create Oauth copy.
        (self.gauth, self.drive) = tools.copy_drive(gauth)
        return

    def run(self):
        print "Thread {} started.\n".format(self.index)
        self.upload_file()
        print "Thread {} finished.\n".format(self.index)
        # Delete file.
        os.remove(self.upload_name)
        return

    def upload_file(self):
        up_file = self.drive.CreateFile(self.params)
        up_file.SetContentFile('encoded_{}.csv'.format(self.index))
        start = time.time()
        up_file.Upload({'convert': True}),
        end = time.time()
        m, s = divmod(end - start, 60)
        print "Upload {}: done. Time: {}m {}s\n".format(self.index, m, s)
