import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import io

SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly","https://www.googleapis.com/auth/drive.readonly"]

def build_drive_service(isServiceAccount=True):
    creds = None
    if isServiceAccount:
        service_account_json_key = "serviceAccountCredentials.json"
        creds = service_account.Credentials.from_service_account_file(filename=service_account_json_key, scopes=SCOPES)
    else:
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def get_next_batch(service, page_token=None):
    results = (
        service.files()
        .list(pageToken=page_token, pageSize=100, fields="nextPageToken, files(id, name, fileExtension, mimeType)")
        .execute()
    )
    items = results.get("files", [])
    nextPageToken = results.get("nextPageToken")
    return items, nextPageToken

def get_image(service, id):
    return io.BytesIO(service.files().get_media(fileId=id).execute())