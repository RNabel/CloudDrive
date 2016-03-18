import unittest
import os

import secrets
from encryption_simple import Encryptor

class EncrytorTest(unittest.TestCase):
    def setUp(self):
        super(EncrytorTest, self).setUp()
        self.encryptor = Encryptor(secrets.password)
        self.encryptor.cipher_storage.create_cipher()

    def test_string_encryption(self):
        data = "hello"
        encrypted = self.encryptor.encrypt(data, string=True)
        decrypted = self.encryptor.decrypt(encrypted, string=True)

        self.assertEqual(data, decrypted)

    def test_file_name_encryption(self):
        data = "hello"
        encrypted = self.encryptor.encrypt(data, file_name=True)
        decrypted = self.encryptor.decrypt(encrypted, file_name=True)

        self.assertEqual(data, decrypted)

    def test_file_encryption_in_place(self):
        file_name = "test_file"
        data = "test data here..."
        if os.path.exists(file_name):
            self.fail("File with name {} exists.".format(file_name))

        file_ptr = open(file_name, mode="w+")
        file_ptr.write(data)
        file_ptr.flush()

        passed = False
        try:
            self.encryptor.encrypt(file_name, is_file=True)
            # file_ptr.seek(0)
            # encrypted = file_ptr.read()
            # self.assertFalse(encrypted == data)
            self.encryptor.decrypt(file_name, is_file=True)
            file_ptr.seek(0)
            decrypted = file_ptr.read()
            self.assertEqual(data, decrypted, "Decrypted text does not equal the original text.")
            passed = True
        finally:
            os.remove(file_name)
            self.assertTrue(passed)

    def test_file_encryption_encryption_different_file(self):
        file_in = "test_file.in"
        file_out = "test_file.out"
        data = "test data here..."

        if os.path.exists(file_in) or os.path.exists(file_out):
            self.fail("File with name {} or {} exists.".format(file_in, file_out))

        file_ptr = open(file_in, mode="w+")
        file_ptr.write(data)
        file_ptr.flush()

        passed = False

        try:
            self.encryptor.encrypt(file_in, is_file=True, target_path=file_out)
            # file_ptr.seek(0)
            # encrypted = file_ptr.read()
            # self.assertFalse(encrypted == data)
            self.encryptor.decrypt(file_out, is_file=True)
            file_ptr = open(file_out)
            decrypted = file_ptr.read()
            self.assertEqual(data, decrypted, "Decrypted text does not equal the original text.")
            passed = True
        finally:
            os.remove(file_in)
            os.remove(file_out)
            self.assertTrue(passed, "Tests did not pass.")

    def test_encryption_decryption_in_different_file(self):
        file_in = "ttest_file.in"
        file_out = "test_file.out"
        data = "test data here..."

        if os.path.exists(file_in) or os.path.exists(file_out):
            self.fail("File with name {} or {} exists.".format(file_in, file_out))

        file_ptr = open(file_in, mode="w+")
        file_ptr.write(data)
        file_ptr.flush()

        passed = False

        try:
            self.encryptor.encrypt(file_in, is_file=True)
            # file_ptr.seek(0)
            # encrypted = file_ptr.read()
            # self.assertFalse(encrypted == data)
            self.encryptor.decrypt(file_in, is_file=True, target_path=file_out)
            file_ptr = open(file_out)
            decrypted = file_ptr.read()
            self.assertEqual(data, decrypted, "Decrypted text does not equal the original text.")
            passed = True
        finally:
            os.remove(file_in)
            os.remove(file_out)
            self.assertTrue(passed, "Tests did not pass.")

