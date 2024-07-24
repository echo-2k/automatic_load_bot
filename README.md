# automatic_load_bot - Скрипт который загружает файлы каждые 30 минут и отправляет ссылки на них в Telegram. 

Установка библиотек

pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-telegram-bot

# Настройка Google Drive API:
Потребуется создать проект в Google Cloud Console и включить Google Drive API.
Сгенерировать файл учетных данных (service account JSON) и скачать его.
Указать ID папки в Google Drive, куда будут загружаться файлы.

# Настройка Telegram бота:
Создать бота через BotFather в Telegram и получить токен.
Получить Chat ID, куда будут отправляться уведомления "https://api.telegram.org/bot<TOKEN>/getUpdates").

# Для создания исполняемого файла будем ипользовать библиотеку pyinstaller

Установка библиотеки
pip install pyinstaller
Исполняемый файл находится в директории dist.
чтобы остановить бота использовать комбинацию клавиш Ctrl+C в терминале.

# Для Windows

1. Открыть командную строку.
2. Перейти в директорию с скриптом.
3. Выполнить команду: pyinstaller --onefile bot.py


# Для Linux

1. Открыть терминал.
2. Перейти в директорию с скриптом.
3. Выполните команду: pyinstaller --onefile bot.py

