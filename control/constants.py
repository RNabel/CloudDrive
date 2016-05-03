# Remote storage constants.
import os
import secrets

FILE_PATH_SEPARATOR = "/"  # Remote file path separator.

PROJECT_FOLDER = secrets.PROJECT_FOLDER

# Encryption related constants.
ENCRYPTED_FLAG = "encrypted"
DECRYPTED_TITLE = "decrypted_title"

ENCRYPTED_FOLDER_PATH = os.path.expanduser("~/Temp/Encrypted")
DECRYPTED_FOLDER_PATH = os.path.expanduser("~/Temp/Decrypted")

VALIDATED_CREDENTIAL_FILE = "/validated_credentials.txt"

UPDATE_INTERVAL = 30  # Number of seconds for file tree sync with remote.

block_size = 524288

assert ENCRYPTED_FLAG != DECRYPTED_TITLE
