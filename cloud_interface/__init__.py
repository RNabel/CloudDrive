from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import control.constants

# Necessary since tests and experiments are run from different contexts.
assert control.constants.PROJECT_FOLDER

gauth = GoogleAuth(settings_file=control.constants.PROJECT_FOLDER + '/cloud_interface/settings.yaml')
# Try to load saved client credentials
CREDENTIALS = control.constants.PROJECT_FOLDER + "/mycreds.txt"
gauth.LoadCredentialsFile(CREDENTIALS)

if gauth.credentials is None:
    # Authenticate if they're not there.
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired.
    gauth.Refresh()
else:
    # Initialize the saved credentials.
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile(CREDENTIALS)

drive = GoogleDrive(gauth)

