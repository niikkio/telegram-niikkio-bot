##### @niikkio_bot
1. Конвертирует и сохраняет все аудиосообщения в формат wav с частотой дискретизации 16kHz
2. Определяет есть ли лицо на фотографиях из диалогов и сохраняет только те, где оно есть

##### Заметки по архитектуре:

1. Поддерживаемые *content_type*: *audio*, *voice*, *photo*.   
2. Для каждого *content_type* определяются *handlers* (обработчики файлов такого типа).  
3. Для каждого *handler* определяются *writers* (варианты сохранения результатов).  
4. Доступно сохранение в файловую систему и в базу MongoDB.
5. Конвертация аудио с помощью библиотеки *librosa*.
6. Анализ фотографий с помощью библиотеки *opencv*.
7. [Предобученные классификаторы](https://github.com/opencv/opencv/tree/master/data).

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

##### TODOs:
1. Алгоритмы определения лиц (research).
2. Использовать [tempfile](https://docs.python.org/3/library/tempfile.html)

