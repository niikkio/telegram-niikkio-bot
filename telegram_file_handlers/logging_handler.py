import logging
from .base_handler import BaseHandler


class LoggingHandler(BaseHandler):
    def handle(self, user_id, temp_filename):
        message = f'Handle entity: user_id={user_id}, temp_file={temp_filename}'
        logging.getLogger('niikkio').info(message)
