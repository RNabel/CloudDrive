"""
Class which wraps the functionality of an individual upload.
"""
import time
import threading
import uuid
from cloud_interface import gauth
from control import tools


class UploadWorkerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name,
                                  verbose=verbose)
        self.args = args
        self.kwargs = kwargs
        self.index = self.kwargs['index']
        self.id = self.kwargs['id']

        # Create Oauth copy.
        print "Create oauth"
        (self.gauth, self.drive) = tools.copy_drive(gauth)
        return

    def run(self):
        print "Thread {} started.\n".format(self.index)
        self.upload_file_worker()
        print "Thread {} finished.\n".format(self.index)
        return

    def upload_file_worker(self):
        i = self.index
        params = {'title': 'test_upload_{}.csv'.format(i),
                  'parents': [{"kind": "drive#fileLink", "id": '0B46HJMu9Db4xTUxhQ0x4WHpfVmM'}],
                  'mimeType': 'text/csv',
                  'properties': [{"value": (str(self.id)), "key": "CloudDrive", "visibility": "PUBLIC"}]
                  }
        up_file = self.drive.CreateFile(params)
        up_file.SetContentFile('encoded_{}.csv'.format(i + 1))
        start = time.time()
        print "Uploading: {}...\n".format(i)
        up_file.Upload({'convert': True}),
        print "Upload {}: done\n".format(i)
        end = time.time()
        m, s = divmod(end - start, 60)
        print "Time taken: ", m, "m ", s, "s"
