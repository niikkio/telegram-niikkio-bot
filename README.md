##### @niikkio_bot
1. Конвертирует и сохраняет все аудиосообщения в формат wav с частотой дискретизации 16kHz
2. Определяет есть ли лицо на фотографиях из диалогов и сохраняет только те, где оно есть

##### Запуск:
```Bash
# Required:
# 1. ffmpeg library
# 2. config/haarcascade_frontalface_default.xml
# 3. config/haarcascade_eye.xml
# 4. config/config.ini
cd telegram-niikkio-bot
virtualenv -p python3 venv
. venv/bin/activate
pip install -r requirements.txt
bash start.sh
```
##### Формат конфигурационного файла:
```
[COMMON]
HOME = /telegram-niikkio-bot
TEMP = /temp/niikkio

[TELEGRAM]
# TELEGRAM API TOKEN HERE:
API_TOKEN = ...

[MONGO]
# MONGODB CREDENTIALS HERE:
USERNAME = ... 
PASSWORD = ...
```

##### Заметки по архитектуре:

1. Поддерживаемые *content_type*: *audio*, *voice*, *photo*.   
2. Для каждого *content_type* определяются *handlers* (обработчики файлов такого типа).  
3. Для каждого *handler* определяются *writers* (варианты сохранения результатов).  
4. Доступно сохранение в файловую систему и в базу MongoDB.
5. Конвертация аудио с помощью библиотеки *librosa*.
6. Анализ фотографий с помощью библиотеки *opencv*.
7. Используются [предобученные классификаторы](https://github.com/opencv/opencv/tree/master/data).

##### TODOs:
1. Алгоритмы определения лиц.
2. Использовать [tempfile](https://docs.python.org/3/library/tempfile.html)
3. Конкретизировать отлавливаемые исключения.

