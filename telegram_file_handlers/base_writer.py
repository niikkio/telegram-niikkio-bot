from abc import abstractmethod


class BaseWriter:
    def __init__(self, category):
        self._category = category

    @abstractmethod
    def save(self, user_id, source_filename):
        """save entity"""
