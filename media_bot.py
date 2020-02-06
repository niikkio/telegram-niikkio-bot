import telebot
import logging
import os
import requests
import shutil
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('niikkio')

h = RotatingFileHandler(filename='bot.log', maxBytes=100000, backupCount=10)
fmt = '%(asctime)s:%(name)s:%(levelname)s: %(message)s'
formatter = logging.Formatter(fmt=fmt)
h.setFormatter(formatter)

logger.addHandler(h)
logger.setLevel(logging.DEBUG)

telebot.logger.handlers = []
telebot.logger.addHandler(h)
telebot.logger.setLevel(logging.DEBUG)


class MediaBot(telebot.TeleBot):
    content_types = {'voice', 'audio', 'photo'}

    extract_file_id = {
        'voice': lambda m: m.voice.file_id,
        'audio': lambda m: m.audio.file_id,
        'photo': lambda m: m.photo[-1].file_id
    }

    def __init__(self, token, temp_path):
        super().__init__(token)
        self._handlers = {content_type: [] for content_type in MediaBot.content_types}
        self._endpoint = f'https://api.telegram.org/file/bot{token}'
        self._temp_path = temp_path

        @self.message_handler(commands=['start'])
        def start_message(message):
            self.send_message(message.chat.id, 'OK')

        @self.message_handler(content_types=['audio', 'photo', 'voice'])
        def content_message(message):
            uid = message.from_user.id
            content_type = message.content_type
            fid = MediaBot.extract_file_id[content_type](message)
            file_path = self.get_file(fid).file_path

            temp_filename = self.download(file_path)
            for handler in self._handlers[content_type]:
                response = handler.handle(uid, temp_filename)
                if response:
                    self.send_message(message.chat.id, response)

            os.remove(temp_filename)

    def add_handler(self, handler, content_types):
        for content_type in content_types:
            self._handlers[content_type].append(handler)

    def download(self, file_path):
        download_url = f'{self._endpoint}/{file_path}'

        def generate_temp_name(url):
            # TODO: use tempfile
            return str(abs(hash(url))) + os.path.splitext(url)[1]

        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
            temp_filename = os.path.join(self._temp_path, generate_temp_name(file_path))
            with open(temp_filename, 'wb') as f_out:
                shutil.copyfileobj(response.raw, f_out)

            return temp_filename
