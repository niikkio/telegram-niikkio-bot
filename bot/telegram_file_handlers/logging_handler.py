import logging

from .base_handler import BaseHandler


class LoggingHandler(BaseHandler):
    """Handler mock: just logging file info"""

    def handle(self, user_id, filename):
        message = f'Handle entity: user_id={user_id}, temp_file={filename}'
        logging.getLogger('niikkio').info(message)
