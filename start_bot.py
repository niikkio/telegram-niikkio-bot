import telebot
import configparser
import logging
from logging.handlers import RotatingFileHandler

from telegram_file_handlers import AudioHandler, MockHandler, PhotoHandler
from telegram_file_handlers import FileWriter, MongoWriter

logger = logging.getLogger('niikkio')


def setup_handlers(bot, token, config):
    url = f'https://api.telegram.org/file/bot{token}'

    mock_handler = MockHandler(url)

    mongo_pattern = r'mongodb+srv://{0}:{1}@niikkio-ihiwe.mongodb.net/test?retryWrites=true&w=majority'
    mongo_connection_string = mongo_pattern.format(
        config['MONGO']['USERNAME'],
        config['MONGO']['PASSWORD']
    )

    temp_path = config['COMMON']['TEMP']
    audio_handler = AudioHandler(url,
                                 [
                                     FileWriter('audio', temp_path),
                                     MongoWriter('audio', mongo_connection_string)
                                 ],
                                 temp_path)

    photo_handler = PhotoHandler(url, [FileWriter('photo', temp_path)], temp_path,
                                 face_cascade_source='config/haarcascade_frontalface_default.xml',
                                 eyes_cascade_source='config/haarcascade_eye.xml')

    handlers = {
        'voice': [mock_handler, audio_handler],
        'audio': [mock_handler, audio_handler],
        'photo': [mock_handler, photo_handler]
    }

    extract_file_id = {
        'voice': lambda m: m.voice.file_id,
        'audio': lambda m: m.audio.file_id,
        'photo': lambda m: m.photo[-1].file_id
    }

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'OK')

    @bot.message_handler(content_types=['audio', 'photo', 'voice'])
    def content_message(message):
        uid = message.from_user.id
        content_type = message.content_type
        fid = extract_file_id[content_type](message)
        file_path = bot.get_file(fid).file_path
        for h in handlers[content_type]:
            response = h.handle(uid, file_path)
            if response:
                bot.send_message(message.chat.id, response)


def start_bot(config):
    token = config['TELEGRAM']['API_TOKEN']
    logger.info(f'TELEGRAM_API_TOKEN={token}')

    bot = telebot.TeleBot(token)

    logger.debug('Setting up handlers...')
    setup_handlers(bot, token, config)

    logger.debug('Starting polling...')
    bot.polling()


def setup_loggers():
    handler = RotatingFileHandler(filename='bot.log', maxBytes=100000, backupCount=10)
    fmt = '%(asctime)s:%(name)s:%(levelname)s: %(message)s'
    formatter = logging.Formatter(fmt=fmt)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    telebot.logger.handlers = []
    telebot.logger.addHandler(handler)
    telebot.logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    conf = configparser.ConfigParser()
    conf.read('config/config.ini')
    setup_loggers()
    start_bot(conf)
