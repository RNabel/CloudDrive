# Remote storage constants.
import os

FILE_PATH_SEPARATOR = "/"  # Remote file path separator.

# Encryption related constants.
ENCRYPTED_FLAG = "encrypted"
DECRYPTED_TITLE = "decrypted_title"

ENCRYPTED_FOLDER_PATH = os.path.expanduser("~/Temp/Encrypted")
DECRYPTED_FOLDER_PATH = os.path.expanduser("~/Temp/Decrypted")

assert ENCRYPTED_FLAG != DECRYPTED_TITLE
