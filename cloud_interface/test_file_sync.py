import os
from unittest import TestCase

from cloud_interface import file_sync
from control import ENC_FOLDER
import structure_fetcher


class TestFileSync(TestCase):
    file_id = "0B-schRXnDFZeYzJiMTZmOTktYjhjNy00YmJlLWE2YTUtZWZkYmQxNzA5ZDBh"

    def test_encrypting_file_upload(self):
        file_sync.sync_file('/home/robin/PycharmProjects/CloudDrive/DESIGN.md', 'root', True)

        # Update metadata.
        structure_fetcher.update_metadata()

        # Ensure file exists
        children = structure_fetcher.get_children('root', False)
        titles = structure_fetcher.get_titles(children)
        self.assertTrue('DESIGN.md' in titles)

    def test_fetch_metadata_after_time(self):
        # Get all metadata.
        structure_fetcher.update_metadata()
        # Modify a file.

        # Get new metadata, and check that new metadata now exists.
        self.fail("Not implemented")

    def test_create_folder(self):
        test_folder_name = 'TEST_FOLDER_TESTSUITE'
        metadata = file_sync._fetch_all_file_info('root')
        all_titles = [f['title'] for f in metadata]
        self.assertTrue(test_folder_name not in all_titles)

        # Create and upload folder.
        file_sync.create_folder(test_folder_name, 'root')

        # Verify folder now exists.
        metadata = file_sync._fetch_all_file_info('root')
        folder_obj = [f for f in metadata if f['title'] == test_folder_name][0]
        self.assertTrue(test_folder_name == folder_obj['title'])

        # Delete folder.
        file_sync._delete_file(folder_obj['id'])
