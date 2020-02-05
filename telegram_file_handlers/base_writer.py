from abc import abstractmethod


class BaseWriter:
    def __init__(self, category):
        self._category = category

    @abstractmethod
    def write(self, user_id, src_filename):
        """save entity"""
