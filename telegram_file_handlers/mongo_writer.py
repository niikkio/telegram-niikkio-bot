from .base_writer import BaseWriter


class MongoWriter(BaseWriter):
    def __init__(self, category, connection_string):
        super().__init__(category)

    def write(self, user_id, src_filename):
        pass
