import logging
from telegram_file_handlers.base_handler import BaseHandler


class MockHandler(BaseHandler):
    def handle(self, category, user_id, file_id):
        message = f'Handle entity: category={category}, uid={user_id}, file_id={file_id}'
        logging.getLogger('niikkio').info(message)
