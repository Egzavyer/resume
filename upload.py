import json
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]

# Get credentials stored in GitHub Secrets
service_account_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])

credentials = service_account.Credentials.from_service_account_info(
    service_account_info,
    scopes=SCOPES,
)

# Create authenticated Google Drive API client
service = build("drive", "v3", credentials=credentials)

# ID of the existing resume.pdf in Google Drive
file_id = os.environ["DRIVE_FILE_ID"]

media = MediaFileUpload(
    "resume.pdf",
    mimetype="application/pdf",
    resumable=True,
)

try:
    updated_file = (
        service.files()
        .update(
            fileId=file_id,
            media_body=media,
            fields="id,name,modifiedTime",
        )
        .execute()
    )

    print(f"Updated {updated_file['name']} " f"at {updated_file['modifiedTime']}")

except Exception as e:
    print(f"An error occurred: {e}")
    raise
