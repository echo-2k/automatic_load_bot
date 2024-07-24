import os
import time
from datetime import datetime
import telegram
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import shutil

TELEGRAM_TOKEN = '123'
CHAT_ID = '123'
FOLDER_ID = '123'
FILES_DIRECTORY = ''
ARCHIVE_NAME = 'files.zip'
SERVICE_ACCOUNT_FILE = ''

SCOPES = ['https://www.googleapis.com/auth/drive.file']
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

bot = telegram.Bot(token=TELEGRAM_TOKEN)

def create_archive(directory, archive_name):
    shutil.make_archive(archive_name.replace('.zip', ''), 'zip', directory)

def upload_files():
    create_archive(FILES_DIRECTORY, ARCHIVE_NAME)
    archive_path = f"{ARCHIVE_NAME}"
    
    file_metadata = {
        'name': ARCHIVE_NAME,
        'parents': [FOLDER_ID]
    }
    media = MediaFileUpload(archive_path, resumable=True)
    request = service.files().create(body=file_metadata, media_body=media, fields='id,webViewLink')
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%.")

    file_id = response.get('id')
    file_link = response.get('webViewLink')
    bot.send_message(chat_id=CHAT_ID, text=f"File downloaded: {ARCHIVE_NAME}\nlink: {file_link}")

def main():
    while True:
        upload_files()
        time.sleep(1800)

if __name__ == '__main__':
    main()
