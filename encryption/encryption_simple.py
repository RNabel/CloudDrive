import encryption.simplecrypt as simplecrypt
import os
import base64
# TODO basic testing, integration into tree_navigation. Can be used to decrypt file names to start with.

class Encryptor:
    def __init__(self, password):
        self.cipher_storage = simplecrypt.create_cipher_storage(password)

    def encrypt(self, data, string=False, file_name=False, file_content=False, origin_path=None, target_path=None):
        if string:
            return simplecrypt.encrypt(self.cipher_storage, data)

        elif file_name:
            file_name_enc = self.encrypt(file_name, string=True)
            file_name_enc = base64.b64encode(file_name_enc)
            file_name_enc = file_name_enc.replace("/", "-")
            return file_name_enc

        elif file_content:
            self._encrypt_file_content(origin_path, target_path)

    def decrypt(self, data, string=False, file_name=False, file_content=False, origin_path=None, target_path=None):
        if string:
            return simplecrypt.decrypt(self.cipher_storage, data)
        elif file_name:
            data = data.replace("-", "/")
            data = base64.b64decode(data)
            try:
                file_name_dec = self.decrypt(data, string=True)
                return file_name_dec
            except Exception as e:
                return False  # If file-name could not be decrypted, return false.

        elif file_content:
            self._decrypt_file(origin_path, target_path)

    # Helper methods.
    def _encrypt_file_content(self, origin_path, target_path):
        # Encrypt file content.
        with open(origin_path, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, string=True)

        # Save result.
        with open(target_path, 'wb') as fo:
            fo.write(enc)

    def _decrypt_file(self, origin_path, target_path):
        # Decrypt file contents.
        with open(origin_path, 'rb') as fo:
            cipher_text = fo.read()
        dec = self.decrypt(cipher_text, string=True)

        with open(target_path, 'wb') as fo:
            fo.write(dec)

# def encrypt_file(self, origin_path, destination_path):
#
#
# def encrypt_file(file_path, key, output_folder=None):
#     file_name = os.path.basename(file_path)
#     folder_path = os.path.dirname(file_path)
#
#     # Encrypt file content.
#     with open(file_path, 'rb') as fo:
#         plaintext = fo.read()
#     enc = simplecrypt.encrypt(key, plaintext)
#
#     # Encrypt name.
#     file_name_enc = encrypt_file_name(file_name, key)
#
#     # Find output folder.
#     output_path = output_folder if output_folder else folder_path
#     output_path += "/" + file_name_enc
#
#     # Encrypt file name.
#     with open(output_path, 'wb') as fo:
#         fo.write(enc)
#
#     return output_path
#
#
# def decrypt_file(file_path, key, output_folder=None):
#     file_name = os.path.basename(file_path)
#     folder_path = os.path.dirname(file_path)
#
#     # Decrypt file contents.
#     with open(file_path, 'rb') as fo:
#         cipher_text = fo.read()
#     dec = simplecrypt.decrypt(key, cipher_text)
#
#     # Decrypt file name.
#     file_name_dec = decrypt_file_name(file_name, key)
#
#     # Find output folder.
#     output_path = output_folder if output_folder else folder_path
#     output_path += "/" + file_name_dec
#     with open(output_path, 'wb') as fo:
#         fo.write(dec)
#
#     return output_path
#
#
# def encrypt_file_name(file_name, key):
#     file_name_enc = encrypt(file_name, key)
#     file_name_enc = base64.b64encode(file_name_enc)
#     file_name_enc = file_name_enc.replace("/", "-")
#     return file_name_enc
#
#
# def decrypt_file_name(file_name, key):
#     file_name = file_name.replace("-", "/")
#     file_name = base64.b64decode(file_name)
#     file_name_dec = decrypt(file_name, key)
#
#     return file_name_dec
