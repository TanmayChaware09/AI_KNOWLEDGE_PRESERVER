SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly"
]

import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from pathlib import Path

SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly"
]


def authenticate_drive():

    creds = None

    base_dir = Path(__file__).resolve().parent.parent

    token_path = base_dir / "drive_token.json"
    client_secret_path = base_dir / "client_secret.json"

    if token_path.exists():

        creds = Credentials.from_authorized_user_file(
            str(token_path),
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                str(client_secret_path),
                SCOPES
            )

            creds = flow.run_local_server(
                port=8081
            )

        with open(
            token_path,
            "w"
        ) as token:

            token.write(
                creds.to_json()
            )

    return build(
        "drive",
        "v3",
        credentials=creds
    )
def get_latest_meeting():

    service = authenticate_drive()

    results = service.files().list(
        q="(mimeType='video/mp4' or mimeType='audio/mpeg' or mimeType='audio/mp3' or mimeType='audio/wav') and trashed=false",
        orderBy="createdTime desc",
        pageSize=1,
        fields="files(id,name,mimeType,createdTime)"
    ).execute()

    files = results.get("files", [])

    if not files:
        return None

    return files[0]

from googleapiclient.http import MediaIoBaseDownload
import io


def download_file(file_id, file_name):

    service = authenticate_drive()

    request = service.files().get_media(fileId=file_id)

    fh = io.FileIO(
        f"meeting/recordings/{file_name}",
        "wb"
    )

    downloader = MediaIoBaseDownload(
        fh,
        request
    )

    done = False

    while not done:
        status, done = downloader.next_chunk()

    print(f"\nDownloaded: {file_name}")