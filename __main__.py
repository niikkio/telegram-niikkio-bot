"""Start telegram bot for media files processing"""
import argparse
import configparser
import logging
import os

from media_bot import MediaBot
from telegram_file_handlers import AudioHandler, LoggingHandler, PhotoHandler
from telegram_file_handlers import FileWriter, MongoWriter


# noinspection PyBroadException
def main():
    logger = logging.getLogger('niikkio')

    # Parse command line arguments:
    parser = argparse.ArgumentParser(description='Bot for media files processing.', add_help=True)

    required = parser.add_argument_group('required arguments')
    required.add_argument('--config', help='configuration file', required=True)

    args = parser.parse_args()

    # Load configuration file:
    config = configparser.ConfigParser()
    config.read(args.config)

    home_path = config['COMMON']['HOME']
    temp_path = config['COMMON']['TEMP']

    bot = MediaBot(token=config['TELEGRAM']['API_TOKEN'],
                   temp_path=temp_path)

    logger.debug('Setting up handlers...')

    # LoggingHandler setup:
    logging_handler = LoggingHandler()
    bot.add_handler(logging_handler, ['voice', 'audio', 'photo'])

    # AudioHandler setup:
    audio_writers = [FileWriter('audio', temp_path)]
    try:
        mongo_pattern = r'mongodb+srv://{0}:{1}@niikkio-ihiwe.mongodb.net/test?retryWrites=true&w=majority'
        mongo_connection_string = mongo_pattern.format(
            config['MONGO']['USERNAME'],
            config['MONGO']['PASSWORD']
        )
        mongo_writer = MongoWriter('audio', mongo_connection_string)

    except Exception:
        logger.error('Failed connecting to MongoDB', exc_info=True)

    else:
        audio_writers.append(mongo_writer)

    audio_handler = AudioHandler(writers=audio_writers)
    bot.add_handler(audio_handler, ['voice', 'audio'])

    # PhotoHandler setup:
    try:
        face_cs = os.path.join(home_path, 'config', 'haarcascade_frontalface_default.xml')
        eyes_cs = os.path.join(home_path, 'config', 'haarcascade_eye.xml')
        photo_handler = PhotoHandler(writers=[FileWriter('photo', temp_path)],
                                     face_cascade_source=face_cs,
                                     eyes_cascade_source=eyes_cs)
    except Exception:
        logger.error('Failed configuring PhotoHandler', exc_info=True)

    else:
        bot.add_handler(photo_handler, ['photo'])

    logger.debug('Starting polling...')
    bot.polling()


main()
