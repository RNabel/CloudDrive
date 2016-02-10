from unittest import TestCase

import encryption.encryption_simple


class TestFileSync(TestCase):
    def test_file_name_encryption(self):
        FILE_NAME = "sample_file.txt"
        PASSWORD = "sample_password"
        encrypted_name = encryption.encryption_simple.encrypt_file_name(FILE_NAME, PASSWORD)
        decrypted_name = encryption.encryption_simple.decrypt_file_name(encrypted_name, PASSWORD)

        self.assertTrue(decrypted_name == FILE_NAME)
