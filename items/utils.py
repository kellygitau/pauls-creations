# utils.py
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_google_drive(file_path, file_name):
    # Set up Google Drive API credentials
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'service_account_credentials.json'  # Replace with your service account credentials file
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Create a Google Drive service object
    service = build('drive', 'v3', credentials=credentials)

    # Upload the file to Google Drive
    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, mimetype='application/octet-stream')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # Print the file ID
    print('File ID:', file.get('id'))

    # Optionally, you can return the file ID or perform additional actions as needed
    return file.get('id')
