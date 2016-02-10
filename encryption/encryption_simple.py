import simplecrypt
import os
import urllib
import base64


def encrypt_file(file_path, key, output_folder=None):
    file_name = os.path.basename(file_path)
    folder_path = os.path.dirname(file_path)

    # Encrypt file content.
    with open(file_path, 'rb') as fo:
        plaintext = fo.read()
    enc = simplecrypt.encrypt(key, plaintext)

    # Encrypt name.
    file_name_enc = encrypt_file_name(file_name, key)

    # Find output folder.
    output_path = output_folder if output_folder else folder_path
    output_path += "/" + file_name_enc

    # Encrypt file name.
    with open(output_path, 'wb') as fo:
        fo.write(enc)

    return output_path


def decrypt_file(file_path, key, output_folder=None):
    file_name = os.path.basename(file_path)
    folder_path = os.path.dirname(file_path)

    # Decrypt file contents.
    with open(file_path, 'rb') as fo:
        cipher_text = fo.read()
    dec = simplecrypt.decrypt(key, cipher_text)

    # Decrypt file name.
    file_name_dec = decrypt_file_name(file_name, key)

    # Find output folder.
    output_path = output_folder if output_folder else folder_path
    output_path += "/" + file_name_dec
    with open(output_path, 'wb') as fo:
        fo.write(dec)

    return output_path


def encrypt_file_name(file_name, key):
    file_name_enc = encrypt(file_name, key)
    file_name_enc = file_name_enc.replace("/", "-")
    return base64.b64encode(file_name_enc)


def decrypt_file_name(file_name, key):
    file_name = file_name.replace("-", "/")
    file_name = base64.b64decode(file_name)
    file_name_dec = decrypt(file_name, key)

    return file_name_dec


def encrypt(input_string, key):
    return simplecrypt.encrypt(key, input_string)


def decrypt(input_string, key):
    return simplecrypt.decrypt(key, input_string)
