from abc import abstractmethod


class BaseHandler:
    def __init__(self, writers=None):
        self._writers = writers

    def _save(self, user_id, temp_filename):
        if self._writers is not None:
            for w in self._writers:
                w.save(user_id, temp_filename)

    @abstractmethod
    def handle(self, user_id, temp_filename):
        """process entity"""
