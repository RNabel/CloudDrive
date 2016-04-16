import unittest
import os
from filesystem import FileBuffers
import cloud_interface
import control.constants


class TestFileBuffer(unittest.TestCase):
    def test_get_file_path_not_in_storage(self):
        temp_buffer = FileBuffers.FileBuffer('abcdef')
        self.assertFalse(temp_buffer.get_file_path('abc'))

    def test_get_file_path_in_storage(self):
        # Need to have add_file working.
        # Test whether it returns the correct path.
        pass

    def test_add_file(self):
        # Create dummy file, ensure it exists.
        # Ensure no file in buffer files.
        # Run add_file
        # Ensure file not in origin location.
        # Test file in destination location.
        # Test if file added to internal storage.
        # Test if added under correct id.

        # Delete file in destination location
        pass  # TODO

    def test_remove_file(self):
        # Add file to storage.
        # Get file name.
        # Test if file present.

        # run remove_file.

        # Test whether file deleted from folder.
        # Test whether file not in data storage.
        pass  # TODO

    def test_create_file_name(self):
        # Create GoogleDriveFile with arbitrary id.
        # run id_to_file_name.
        # Test if created file name is contained in create_file_name result.
        #       has to be at end, so endswith.
        pass  # TODO

    def test_id_to_name(self):
        file_id = "abcd-abd"
        temp_buffer = FileBuffers.FileBuffer('abcdef')
        file_name = temp_buffer.id_to_file_name(file_id)
        self.assertEqual(temp_buffer.file_name_to_id(file_name), file_id)

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
