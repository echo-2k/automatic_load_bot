import os
import time
from datetime import datetime
import telegram
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Параметры
FOLDER_ID = 'your_google_drive_folder_id'  # Замените на ваш ID папки в Google Drive
TELEGRAM_TOKEN = 'your_telegram_bot_token'  # Замените на ваш токен бота Telegram
CHAT_ID = 'your_chat_id'  # Замените на ваш Chat ID
FILES_DIRECTORY = '/path/to/your/files'  # Замените на путь к папке с файлами

# Настройка Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'path/to/your/service-account-file.json'  # Замените на путь к вашему файлу учетных данных

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

# Настройка Telegram бота
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
            media = MediaFileUpload(file_path, mimetype='application/octet-stream')
            uploaded_file = service.files().create(body=file_metadata, media_body=media, fields='id,webViewLink').execute()
            file_id = uploaded_file.get('id')
            file_link = uploaded_file.get('webViewLink')
            bot.send_message(chat_id=CHAT_ID, text=f"Файл загружен: {file_name}\nСсылка: {file_link}")

def main():
    while True:
        upload_files()
        time.sleep(1800)  # Пауза 30 минут

if __name__ == '__main__':
    main()
  
