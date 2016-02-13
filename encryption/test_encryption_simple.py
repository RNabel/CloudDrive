from unittest import TestCase
import control.secrets

import encryption.encryption_simple


class TestFileSync(TestCase):
    def test_file_name_encryption(self):
        FILE_NAME = "sample_file.txt"
        PASSWORD = control.secrets.PASSWORD
        encrypted_name = encryption.encryption_simple.encrypt_file_name(FILE_NAME, PASSWORD)
        try:
            decrypted_name = encryption.encryption_simple.decrypt_file_name(encrypted_name, PASSWORD)
        except:
            self.fail("Encrypted name failed:\n{}".format(encrypted_name))

        self.assertTrue(decrypted_name == FILE_NAME)
