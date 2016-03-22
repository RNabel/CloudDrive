import encryption.simplecrypt as simplecrypt
import base64

class Encryptor:
    def __init__(self, password):
        self.cipher_storage = simplecrypt.create_cipher_storage(password)

    def encrypt(self, data, string=False, file_name=False, is_file=False, target_path=None):
        if string:
            return simplecrypt.encrypt(self.cipher_storage, data)

        elif file_name:
            file_name_enc = self.encrypt(data, string=True)
            file_name_enc = base64.b64encode(file_name_enc)
            file_name_enc = file_name_enc.replace("/", "-")
            return file_name_enc

        elif is_file:
            # Data in this case is the file name
            self._encrypt_file_content(data, target_path)

        else:
            raise Exception("No encryption type specified.")

    def decrypt(self, data, string=False, file_name=False, is_file=False, target_path=None):
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

        elif is_file:
            self._decrypt_file(data, target_path)

        else:
            raise Exception("No decryption type specified.")

    # Helper methods.
    def _encrypt_file_content(self, origin_path, target_path):
        # Encrypt file content.
        fi = open(origin_path, 'r+')
        fi.seek(0)
        plaintext = fi.read()
        enc = self.encrypt(plaintext, string=True)

        # Save result.
        if target_path:
            # If output file specified, write into specified file.
            fi = open(target_path, 'w+')

        fi.truncate(0)
        fi.seek(0)
        fi.write(enc)
        fi.flush()

    def _decrypt_file(self, origin_path, target_path):
        # Decrypt file contents.
        fp = open(origin_path, 'r+')
        fp.seek(0)
        cipher_text = fp.read()
        dec = self.decrypt(cipher_text, string=True)

        # Save decrypted.
        if target_path:
            fp = open(target_path, 'w+')

        fp.truncate(0)
        fp.seek(0)
        fp.write(dec)
        fp.flush()
