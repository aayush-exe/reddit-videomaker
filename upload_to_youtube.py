import os
import google.auth
import google.auth.transport.requests
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

# Replace with your OAuth 2.0 credentials file path
CLIENT_SECRETS_FILE = "path/to/your/client_secret.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def upload_video(service, video_file, title, description, category_id, tags):
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": "public"
        }
    }

    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = service.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print("Uploaded %d%%." % int(status.progress() * 100))
    print("Upload Complete!")
    return response

def main():
    service = get_authenticated_service()
    video_file = "path/to/your/video.mp4"
    title = "Your Video Title"
    description = "Your Video Description"
    category_id = "22"  # See https://developers.google.com/youtube/v3/docs/videoCategories/list for category IDs
    tags = ["tag1", "tag2"]

    response = upload_video(service, video_file, title, description, category_id, tags)
    print("Video uploaded successfully. Video ID:", response["id"])

if __name__ == "__main__":
    main()
