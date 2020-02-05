import logging
from telegram_file_handlers.base_handler import BaseHandler


class MockHandler(BaseHandler):
    def handle(self, user_id, file_path):
        message = f'Handle entity: user_id={user_id}, file_path={file_path}'
        logging.getLogger('niikkio').info(message)
