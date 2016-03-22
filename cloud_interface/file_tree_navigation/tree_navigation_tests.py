import unittest

from encryption.encryptor import Encryptor
from cloud_interface.file_tree_navigation import FileTreeState
from pydrive.files import GoogleDriveFile
import secrets

class TestFileTreeNavigation(unittest.TestCase):
    def setUp(self):
        super(TestFileTreeNavigation, self).setUp()

        self.fileTreeState = FileTreeState()

    def test_get_names(self):
        names = ["Name1", "Name2"]
        current_node = dict()
        for name in names:
            gdrive_file = GoogleDriveFile(metadata={'title': name})
            current_node[name] = gdrive_file

        self.fileTreeState.currentNode = current_node

        returned_names = self.fileTreeState.get_names()

        for name in names:
            self.assertTrue(name in returned_names)

    def test_get_names_encrypted(self):
        # Create encrypted names.
        encryptor = Encryptor(secrets.password)
        encryptor.cipher_storage.create_cipher()

        names = ["Name1", "Name2"]
        current_node = dict()

        for name in names:
            encrypted_name = encryptor.encrypt(name, string=True)
            encrypted_gdrive_file = GoogleDriveFile(metadata={'title': encrypted_name})
            current_node[name] = encrypted_gdrive_file

        # Assign the object filled with encrypted titles to the cuurrentNode field
        self.fileTreeState.currentNode = current_node
        # Decrypt the names.
        self.fileTreeState._decrypt_file_names_in_current_folder()
        # Test output.
        returned_names = self.fileTreeState.get_names()

        for name in names:
            self.assertTrue(name in returned_names)

    def test_get_names_encrypted_mixed(self):
                # Create encrypted names.
        encryptor = Encryptor(secrets.password)
        encryptor.cipher_storage.create_cipher()

        names = ["Name1", "Name2"]
        current_node = dict()

        for name in names:
            encrypted_name = encryptor.encrypt(name, string=True)
            encrypted_gdrive_file = GoogleDriveFile(metadata={'title': encrypted_name})
            current_node[name] = encrypted_gdrive_file

        names.append("Name3")
        current_node["Name3"] = GoogleDriveFile(metadata={'title': "Name3"})

        # Assign the object filled with encrypted titles to the cuurrentNode field
        self.fileTreeState.currentNode = current_node
        # Decrypt the names.
        self.fileTreeState._decrypt_file_names_in_current_folder()
        # Test output.
        returned_names = self.fileTreeState.get_names()

        for name in names:
            self.assertTrue(name in returned_names)
