# Remote storage constants.
import os
import secrets

FILE_PATH_SEPARATOR = "/"  # Remote file path separator.

PROJECT_FOLDER = secrets.PROJECT_FOLDER

# Encryption related constants.
ENCRYPTED_FLAG = "encrypted"
DECRYPTED_TITLE = "decrypted_title"

# Settings
# ==========

ENCRYPTED_FOLDER_PATH = os.path.expanduser("~/Temp/Encrypted")
DECRYPTED_FOLDER_PATH = os.path.expanduser("~/Temp/Decrypted")

VALIDATED_CREDENTIAL_FILE = "/validated_credentials.txt"

DRIVE_NAME = "GDriveFileSystem"

UPDATE_INTERVAL = 30  # Number of seconds for file tree sync with remote.

LOGS_FOLDER = "%PROJECT_FOLDER%/logs/"
LOGS_FOLDER = LOGS_FOLDER.replace("%PROJECT_FOLDER%", PROJECT_FOLDER)
# Ensure logs folder exists.
if not os.path.exists(LOGS_FOLDER):
    os.makedirs(LOGS_FOLDER)

block_size = 524288

assert ENCRYPTED_FLAG != DECRYPTED_TITLE
