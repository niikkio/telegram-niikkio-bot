import logging
from telegram_file_handlers.base_handler import BaseHandler

logger = logging.getLogger('niikkio').getChild('photo')


class PhotoHandler(BaseHandler):
    def handle(self, user_id, file_path):
        logger.debug(f'Downloading file: {file_path}...')
        tmp_filename = self._download(file_path)

        logger.debug(f'Saving temp file: {tmp_filename}...')
        self._save(user_id, tmp_filename)
