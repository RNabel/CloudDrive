import os

import encryption_simple
import util
import control.secrets

TEMP_ENC_FOLDER = "/home/robin/PycharmProjects/CloudDrive/temp_enc_folder"
TEMP_DEC_FOLDER = "/home/robin/PycharmProjects/CloudDrive/temp_dec_folder"

PASSWORD = control.secrets.PASSWORD


def encrypt_file(file_name, output_folder=TEMP_ENC_FOLDER):
    """
    Encrypt the file specified with file_name.
    Args:
        file_name: The path of the file to encrypt.
        output_folder: The path of the folder to save the encrypted file to.

    Returns: The name of the encrypted file.

    """
    # Open encrypted output file.
    return encryption_simple.encrypt_file(file_name, PASSWORD, output_folder)


def decrypt_file(file_name, output_folder):
    """
    Decrypt the file specified with file_name.
    Args:
        file_name: The name of the file
        output_folder: The folder to store the file in.

    Returns: The full path of the decrypted file.

    """
    return encryption_simple.decrypt_file(file_name, PASSWORD, output_folder)


def decrypt(input):
    return encryption_simple.decrypt(input, PASSWORD)


def encrypt(input):
    return encryption_simple.encrypt(input, PASSWORD)


def decrypt_file_name(file_name):
    return encryption_simple.decrypt_file_name(file_name, PASSWORD)


def encrypt_file_name(file_name):
    return encryption_simple.encrypt_file_name(file_name, PASSWORD)
