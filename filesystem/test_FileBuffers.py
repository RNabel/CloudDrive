import unittest
import os
from filesystem import FileBuffers
import cloud_interface
import control.constants

class TestEncryptedBuffer(unittest.TestCase):
    def test_initial(self):
        temp_buffer = FileBuffers.EncryptedFileBuffer()
        self.assertFalse(len(temp_buffer.files))
        self.assertTrue(temp_buffer.path == control.constants.ENCRYPTED_FOLDER_PATH)

    def test_download(self):
        file_id = '0B-schRXnDFZebGFCcjYwRkxNN00'
        file_name = 'test_file.txt'
        gdrive_file = cloud_interface.drive.CreateFile({'id': file_id, 'title': file_name})
        temp_buffer = FileBuffers.EncryptedFileBuffer()

        # Ensure FileBuffer is empty.
        self.assertFalse(os.path.exists(file_name))
        self.assertFalse(len(temp_buffer.files))
        temp_buffer.download_file(gdrive_file)
        self.assertTrue(len(temp_buffer.files) == 1)
