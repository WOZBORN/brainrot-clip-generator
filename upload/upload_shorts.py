import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from ..config import (TOKEN_PATH,
                      CLIENT_SECRETS_FILE, SCOPES,
                      API_SERVICE_NAME, API_VERSION,
                      FILE_PATH, TITLE, DESCRIPTION,
                      TAGS, PRIVACY)

def get_authenticated_service():
    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_PATH, 'w') as token_file:
            token_file.write(creds.to_json())

    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES
    )
    auth_url, _ = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    return auth_url


def upload_short(file_path, title, description, tags, privacy="public"):
    if not os.path.isfile(file_path) or not file_path.lower().endswith('.mp4'):
        print(f"Ошибка: файл не найден или не .mp4 — {file_path}")
        return

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    youtube = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=creds
    )

    short_title = f"#shorts #brainrot #брэйнрот #итальянский_брейрот #итальянские_животные".strip()
    short_description = f"{description}\n\n#shorts"
    short_tags = list(set(tags + ["shorts"]))

    body = {
        'snippet': {
            'title': short_title,
            'description': short_description,
            'tags': short_tags,
            'categoryId': '22'
        },
        'status': {
            'privacyStatus': privacy
        }
    }
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype="video/*")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    print(f"Начинаем загрузку: {file_path}")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Progress: {int(status.progress() * 100)}%")

    video_id = response.get('id')
    print(f"Готово! https://youtu.be/{video_id}")
    return video_id


if __name__ == "__main__":
    upload_short(FILE_PATH, TITLE, DESCRIPTION, TAGS, PRIVACY)