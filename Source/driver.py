import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import io

SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly","https://www.googleapis.com/auth/drive.readonly"]

def build_drive_service():
    creds = None
    service_account_json_key = "serviceAccountCredentials.json"
    creds = service_account.Credentials.from_service_account_file(filename=service_account_json_key, scopes=SCOPES)

    try:
        service = build("drive", "v3", credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def get_next_batch(service, page_token=None):
    results = (
        service.files()
        .list(pageToken=page_token, pageSize=10, fields="nextPageToken, files(id, name, fileExtension, mimeType)")
        .execute()
    )
    items = results.get("files", [])
    nextPageToken = results.get("nextPageToken")
    return items, nextPageToken

def get_image(service, id):
    return io.BytesIO(service.files().get_media(fileId=id).execute())