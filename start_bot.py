import telebot
import configparser
import logging
from logging.handlers import RotatingFileHandler

from telegram_file_handlers import MockHandler

logger = logging.getLogger('niikkio')


def setup_handlers(bot):
    mock_handler = MockHandler()
    handlers = {
        'voice': [mock_handler],
        'audio': [mock_handler],
        'photo': [mock_handler]
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
        for h in handlers[content_type]:
            h.handle(content_type, uid, fid)


def start_bot(config):
    token = config['TELEGRAM']['API_TOKEN']
    logger.info(f'TELEGRAM_API_TOKEN={token}')

    bot = telebot.TeleBot(token)

    logger.debug('Setting up handlers...')
    setup_handlers(bot)

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
    conf.read('config.ini')
    setup_loggers()
    start_bot(conf)
