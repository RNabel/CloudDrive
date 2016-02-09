import os
from unittest import TestCase

from cloud_interface import file_sync
from control import ENC_FOLDER


class TestFileSync(TestCase):
    file_id = "0B-schRXnDFZeYzJiMTZmOTktYjhjNy00YmJlLWE2YTUtZWZkYmQxNzA5ZDBh"

    def test_file_download(self):
        file_sync._download_file(self.file_id)

        # Ensure file is present.
        self.assertTrue(os.path.exists(ENC_FOLDER + "/" + self.file_id))

        # Delete file.
        os.remove(ENC_FOLDER + "/" + self.file_id)

    def test_file_upload(self):
        # Get info of uploaded file.

        # Upload file.
        file_sync._upload_file(self.file_id)

        # Get info of newly uploaded file.

        # Test whether access time changed.

        self.fail("Not implemented")

    def test_file_upload_new_file(self):
        # Get info of file.

        # Test that info is null.

        # Create and upload file.
        test_file_path = "test_folder/test_file"
        if os.path.exists(test_file_path):
            self.fail("file already exists!")
        fptr = open(test_file_path, "w+")
        fptr.write("test content.")

        # Get info and check that the file now exists on remote.

        self.fail("Not implemented")

    def test_fetch_metadata_after_time(self):
        # Get all metadata.

        # Modify a file.

        # Get new metadata, and check that new metadata now exists.
        self.fail("Not implemented")

    def test_create_folder(self):
        test_folder_name = 'TEST_FOLDER_TESTSUITE'
        metadata = file_sync._fetch_all_file_info('root')
        all_titles = [f['title'] for f in metadata]
        self.assertTrue(test_folder_name not in all_titles)

        # Create and upload folder.
        file_sync._create_folder(test_folder_name, 'root')

        # Verify folder now exists.
        metadata = file_sync._fetch_all_file_info('root')
        folder_obj = [f for f in metadata if f['title'] == test_folder_name][0]
        self.assertTrue(test_folder_name == folder_obj['title'])

        # Delete folder.
        file_sync._delete_file(folder_obj['id'])
