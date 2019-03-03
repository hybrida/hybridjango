import pickle
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from datetime import datetime
from .secrets import FOLDER_ID  # SEE BELOW
from . import ISO_8601

# This file will throw ImportErrors on the .secrets module except when in production
# This is by design, as the secrets-folder contains sensitive information and is ignored explicitly by Git

# If you desire a local setup of drive-uploads, do the following:
# 1. Create a folder under hybridjango/utils called secrets
# 2. Create a file in that folder called __init__.py
# 3. In that file, add the line FOLDER_ID = $YourGoogleDriveFolderID
# 4. Generate a valid pickled credentials file called token.pickle
# 5. Add token.pickle to the secrets folder

# For further help with step 4, see https://developers.google.com/drive/api/v3/quickstart/python
# Required scopes for credentials file:
# SCOPES = ['https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/drive.file']


def get_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    filename = 'hybridjango/utils/secrets/token.pickle'
    if os.path.exists(filename):
        with open(filename, 'rb') as token:
            creds = pickle.load(token)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    if not creds or not creds.valid:
        return None
    else:
        return build('drive', 'v3', credentials=creds, cache_discovery=False)


def upload_db_backup(filename):
    """
    Uploads a DB backup to Google Drive
    Is used when passing --upload to the backup_db management command
    """
    service = get_service()
    if service is None:
        print("Error with credentials. Terminating.")
        return

    file_metadata = {
        'name': os.path.basename(filename),
        'parents': [FOLDER_ID]
    }
    # no MIME-type means service will guess based on extension
    media = MediaFileUpload(filename, mimetype=None)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    print("Backup successfully uploaded with file ID {}".format(file.get('id')))


def manage_and_delete_backups(cutoff=None, keep_amount=None):
    """
    Check and potentially delete backup files from drive
    :param cutoff: optional timedelta, delete all files older than now - cutoff
    :param keep_amount: optional int, keep at most count files, delete oldest
    :return:
    """
    # TODO this function is still WIP, and is not called from any custom Management Commands
    service = get_service()
    if service is None:
        print("Error with credentials. Terminating.")
        return

    query = "'{}' in parents".format(FOLDER_ID)
    results = service.files().list(
        q=query,
        pageSize=10,
        fields="nextPageToken, files(id, name)"
    ).execute()
    files = sorted(results.get("files", []), key=lambda f: f.get("name"), reverse=True)
    now = datetime.now()
    count = 0
    for file in files:
        filename = file.get("name")
        date, _ = filename.split(".")
        date = date.replace("BACKUP ", "")
        date = datetime.strptime(date, ISO_8601)
        delta = now - date
        if count >= keep_amount:
            print("{}, deleting (age {})".format(filename, delta))
            service.files().delete(fileId=file.get("id")).execute()
        if delta < cutoff:
            print("{}, keeping".format(filename))
        else:
            print("{}, deleting (age {})".format(filename, delta))
            service.files().delete(fileId=file.get("id")).execute()
