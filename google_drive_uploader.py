import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Scopes required for Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']

def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)  # Updated to use client_secret.json
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    service = build('drive', 'v3', credentials=creds)
    return service

def upload_file(service, file_path, file_name, mime_type):
    file_metadata = {'name': file_name}
    media = MediaFileUpload(file_path, mimetype=mime_type)
    file = service.files().create(body=file_metadata, media_body=media, fields='id,webViewLink').execute()
    # print(f'File ID: {file.get("id")}')
    # print(f'File Link: {file.get("webViewLink")}')
    return file.get("id"), file.get("webViewLink")

def make_file_public(service, file_id):
    permission = {
        'type': 'anyone',
        'role': 'reader',
    }
    service.permissions().create(
        fileId=file_id,
        body=permission,
    ).execute()
    # print(f'File ID {file_id} is now public.')

def upload_to_google(file_path, file_name):
    service = authenticate()
    file_id, file_link = upload_file(service, file_path, file_name, 'video/mp4')
    make_file_public(service, file_id)
    file_link = file_link[:-17]+"preview"
    return file_link

# print(upload_to_google("/Users/aayush/Documents/reddit-videomaker/reddit-videomaker/output/08052024,22:01:57,from@agushagush.mp4", "new/new.mp4"))
