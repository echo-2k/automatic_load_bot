import os
import time
from datetime import datetime
import telegram
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

TELEGRAM_TOKEN = '123'
CHAT_ID = '123'
FOLDER_ID = '123'
FILES_DIRECTORY = ''

SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = ''

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

bot = telegram.Bot(token=TELEGRAM_TOKEN)

def upload_files():
    files = os.listdir(FILES_DIRECTORY)
    for file_name in files:
        file_path = os.path.join(FILES_DIRECTORY, file_name)
        if os.path.isfile(file_path):
            file_metadata = {
                'name': file_name,
                'parents': [FOLDER_ID]
            }
            media = MediaFileUpload(file_path, resumable=True)
            request = service.files().create(body=file_metadata, media_body=media, fields='id,webViewLink')
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print(f"Uploaded {int(status.progress() * 100)}%.")

            file_id = response.get('id')
            file_link = response.get('webViewLink')
            bot.send_message(chat_id=CHAT_ID, text=f"File downloaded: {file_name}\nlink: {file_link}")

def main():
    while True:
        upload_files()
        time.sleep(1800)

if __name__ == '__main__':
    main()