import os
from unittest import TestCase

from cloud_interface import file_sync
from control import ENC_FOLDER


class TestFileSync(TestCase):
    def test_file_download(self):
        file_id = "0B-schRXnDFZeYzJiMTZmOTktYjhjNy00YmJlLWE2YTUtZWZkYmQxNzA5ZDBh"
        file_sync._download_file(file_id)

        # Ensure file present
        self.assertTrue(os.path.exists(ENC_FOLDER + "/" + file_id))

        # Delete file.
        os.remove(ENC_FOLDER + "/" + file_id)
