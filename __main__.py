import os
import logging
import argparse
import configparser
from media_bot import MediaBot
from telegram_file_handlers import AudioHandler, LoggingHandler, PhotoHandler
from telegram_file_handlers import FileWriter, MongoWriter


def main():
    logger = logging.getLogger('niikkio')

    parser = argparse.ArgumentParser(description='Bot for media processing.', add_help=True)

    required = parser.add_argument_group('required arguments')
    required.add_argument('--config', help='configuration file', required=True)

    args = parser.parse_args()
    config = configparser.ConfigParser()
    config.read(args.config)

    home_path = config['COMMON']['HOME']
    temp_path = config['COMMON']['TEMP']

    bot = MediaBot(token=config['TELEGRAM']['API_TOKEN'],
                   temp_path=temp_path)

    logger.debug('Setting up handlers...')

    logging_handler = LoggingHandler()

    mongo_pattern = r'mongodb+srv://{0}:{1}@niikkio-ihiwe.mongodb.net/test?retryWrites=true&w=majority'
    mongo_connection_string = mongo_pattern.format(
        config['MONGO']['USERNAME'],
        config['MONGO']['PASSWORD']
    )

    audio_handler = AudioHandler(writers=[
                                     FileWriter('audio', temp_path),
                                     # MongoWriter('audio', mongo_connection_string)
                                 ])

    face_cs = os.path.join(home_path, 'config', 'haarcascade_frontalface_default.xml')
    eyes_cs = os.path.join(home_path, 'config', 'haarcascade_eye.xml')
    photo_handler = PhotoHandler(writers=[FileWriter('photo', temp_path)],
                                 face_cascade_source=face_cs,
                                 eyes_cascade_source=eyes_cs)

    bot.add_handler(logging_handler, ['voice', 'audio', 'photo'])
    bot.add_handler(audio_handler, ['voice', 'audio'])
    bot.add_handler(photo_handler, ['photo'])

    logger.debug('Starting polling...')
    bot.polling()


main()
