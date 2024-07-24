# automatic_load_bot

pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-telegram-bot

Настройка Google Drive API:

Потребуется создать проект в Google Cloud Console и включить Google Drive API.
Сгенерировать файл учетных данных (service account JSON) и скачать его.
Указать ID папки в Google Drive, куда будут загружаться файлы.

Настройка Telegram бота:

Создать бота через BotFather в Telegram и получить токен.
Получить Chat ID, куда будут отправляться уведомления (например, с помощью curl "https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates").

Функция upload_files():

Загружает все файлы из указанной директории в Google Drive.
Отправляет сообщение в Telegram с ссылкой на каждый загруженный файл.
Основной цикл в функции main():

Выполняет функцию upload_files() каждые 30 минут с помощью time.sleep(1800).



Этот скрипт будет загружать файлы каждые 30 минут и отправлять ссылки на них в Telegram. 
