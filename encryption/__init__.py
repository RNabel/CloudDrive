import os

import name_encryption
import file_encryption
import util

TEMP_FOLDER = "/home/robin/PycharmProjects/CloudDrive/temp_folder"
PASSWORD = util.get_password()


def encrypt_file(name):
    # Create file object.
    file_in = open(name)
    file_base_name = os.path.basename(file_in.name)

    # Create encrypted name.
    file_out_name = name_encryption.encrypt(PASSWORD[:32], file_base_name)
    file_out_name = TEMP_FOLDER + "/" + file_out_name

    # Open encrypted output file. TODO ensure file does not exist.
    file_out = open(file_out_name, "wr+")
    file_encryption.encrypt(file_in, file_out, PASSWORD, 32)


def decrypt_file(name):
    # Create file object.
    file_in = open(name)

    # Create encrypted name.
    file_out_name = name_encryption.decrypt(PASSWORD[:32], file_in.name)
    file_out_name = TEMP_FOLDER + "/" + file_out_name

    # Open encrypted output file. TODO ensure file does not exist.
    file_out = open(file_out_name, "w")
    file_encryption.decrypt(file_in, file_out, PASSWORD, 32)
