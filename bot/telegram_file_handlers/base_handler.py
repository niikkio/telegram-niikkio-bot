from abc import abstractmethod


class BaseHandler:
    """Abstract class to handle media file from user"""
    def __init__(self, writers=None):
        self._writers = writers

    def _save(self, user_id, filename):
        if self._writers is not None:
            for w in self._writers:
                w.save(user_id, filename)

    @abstractmethod
    def handle(self, user_id, filename):
        """Process media file"""
