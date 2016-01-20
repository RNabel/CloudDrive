from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
# Try to load saved client credentials
CREDENTIALS = "/home/robin/PycharmProjects/CloudDrive/cloud_interface/mycreds.txt"
gauth.LoadCredentialsFile(CREDENTIALS)
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile(CREDENTIALS)

drive = GoogleDrive(gauth)

