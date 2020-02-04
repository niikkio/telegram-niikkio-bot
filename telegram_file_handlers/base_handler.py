from abc import abstractmethod


class BaseHandler:
    @abstractmethod
    def handle(self, category, user_id, file_id):
        """process entity"""
