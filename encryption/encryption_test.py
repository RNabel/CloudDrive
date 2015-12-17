import encryption
import encryption.name_encryption
import encryption.file_encryption
import encryption.util
import os

if __name__ == "__main__":
    password = encryption.util.get_password()

    # Testing name encryption.
    testName = "Hello.docx"
    encryptedName = encryption.name_encryption.encrypt(password, testName)
    decryptedName = encryption.name_encryption.decrypt(password, encryptedName)
    assert testName == decryptedName

    # Test file encryption and decryption.
    file_name = "test_file.txt"
    file_test_string = "1234567890ABCdef!@#$%^&*("
    fptr = open(file_name, "w+")
    fptr.seek(0)
    fptr.write(file_test_string)
    fptr.flush()
    fptr.seek(0)
    file_content = fptr.readline()
    assert file_test_string == file_content  # Assert successful write action

    encryption.file_encryption.encrypt_file(password, file_name)
    encryption.file_encryption.decrypt_file(password, file_name + ".enc", file_name + ".dec")

    # Read from both files, and compare results.
    original_file = open(file_name, "r")
    decrypted_file = open(file_name + ".dec", "r")
    assert original_file.readline() == decrypted_file.readline()

    # Tear-down
    os.remove(file_name)
    os.remove(file_name + ".dec")
    os.remove(file_name + ".enc")

    # Test end-to-end.
    test_file_name = "../README.md"
    encrypted_name = encryption.encrypt_file(test_file_name)

    decrypted_name = encryption.decrypt_file(encrypted_name)

    # Check content correct.
    original_file = open(test_file_name)
    decrypted_file = open(decrypted_name)

    assert original_file.read() == decrypted_file.read()

    os.remove(encrypted_name)
    os.remove(decrypted_name)
