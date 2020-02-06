from abc import abstractmethod


class BaseWriter:
    """Abstract class to save media file"""
    def __init__(self, category):
        self._category = category

    @abstractmethod
    def save(self, user_id, source_filename):
        """Save media file"""
