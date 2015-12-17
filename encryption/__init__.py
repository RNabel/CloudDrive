import os
import name_encryption
import file_encryption
import util

TEMP_ENC_FOLDER = "/home/robin/PycharmProjects/CloudDrive/temp_enc_folder"
TEMP_DEC_FOLDER = "/home/robin/PycharmProjects/CloudDrive/temp_dec_folder"

PASSWORD = util.get_password()


def encrypt_file(file_name):
    """
    :param file_name: The name of the file to encrypt.
    :return: The name of the encrypted file.
    """
    # Create encrypted name.
    file_base_name = os.path.basename(file_name)
    file_out_name = name_encryption.encrypt(PASSWORD, file_base_name)
    file_out_name = TEMP_ENC_FOLDER + "/" + file_out_name

    # Open encrypted output file.
    file_encryption.encrypt_file(PASSWORD, file_name, file_out_name)
    return file_out_name


def decrypt_file(name):
    # Create encrypted name.
    file_name = os.path.split(name)[1]
    file_out_name = name_encryption.decrypt(PASSWORD, file_name)
    file_out_name = TEMP_DEC_FOLDER + "/" + file_out_name

    # Open encrypted output file.
    file_encryption.decrypt_file(PASSWORD, name, file_out_name)

    return file_out_name
