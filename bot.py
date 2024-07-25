import os
import time
from datetime import datetime
import telegram
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pyzipper

TELEGRAM_TOKEN = '123'
CHAT_ID = '123'
FOLDER_ID = '123'
FILES_DIRECTORY = ''
ARCHIVE_NAME = 'files.zip'
# ARCHIVE_PASSWORD = 'password'
SERVICE_ACCOUNT_FILE = ''

SCOPES = ['https://www.googleapis.com/auth/drive.file']
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

bot = telegram.Bot(token=TELEGRAM_TOKEN)

# def create_archive_with_password(directory, archive_name, password):
#     with pyzipper.AESZipFile(archive_name, 'w', compression=pyzipper.ZIP_DEFLATED) as zf:
#         zf.setpassword(password.encode())
#         for foldername, subfolders, filenames in os.walk(directory):
#             for filename in filenames:
#                 file_path = os.path.join(foldername, filename)
#                 arcname = os.path.relpath(file_path, start=directory)
#                 zf.write(file_path, arcname)

def create_archive(directory, archive_name):
    try:
        with pyzipper.AESZipFile(archive_name, 'w', compression=pyzipper.ZIP_DEFLATED) as zf:
            for foldername, subfolders, filenames in os.walk(directory):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(file_path, start=directory)
                    print(f"Adding {file_path} as {arcname} to archive")
                    zf.write(file_path, arcname)
        print(f"Archive {archive_name}")
    except Exception as e:
        print(f"Failed: {e}")

async def upload_files():
    create_archive_with_password(FILES_DIRECTORY, ARCHIVE_NAME, ARCHIVE_PASSWORD)
    archive_path = ARCHIVE_NAME
    
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

    if response:
        file_id = response.get('id')
        file_link = response.get('webViewLink')
        await bot.send_message(chat_id=CHAT_ID, text=f"File uploaded: {ARCHIVE_NAME}\nLink: {file_link}\nPassword: {ARCHIVE_PASSWORD}")
    else:
        print("Failed to upload file.")

async def main():
    while True:
        await upload_files()
        await asyncio.sleep(1800)

if __name__ == '__main__':
    asyncio.run(main())
