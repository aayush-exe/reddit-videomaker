import os
import google.auth
import google.auth.transport.requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Scopes required for YouTube Data API
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def authenticate():
    # Authenticate the user and return the service object.
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    service = build('youtube', 'v3', credentials=creds)
    return service

def upload_video(service, video_file, title, description, tags, privacy_status):
    # Upload video to YouTube.
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
        },
        'status': {
            'privacyStatus': privacy_status
        }
    }
    
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = service.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if response is not None and 'id' in response:
            print(f"Video id '{response['id']}' was successfully uploaded.")
        elif status:
            print(f"Upload status: {status.progress() * 100:.2f}%")
        else:
            print(f"The upload failed with an unexpected response: {response}")

def upload_to_yt(video_file, title, description):
    tags = ['mogus','bogus','meow']
    privacy_status = 'unlisted'  # or 'public' or 'unlisted'

    service = authenticate()
    upload_video(service, video_file, title, description, tags, privacy_status)

upload_to_yt('output/08052024,18:15:18,from@agushagush.mp4', "testing", "maiden journey")
