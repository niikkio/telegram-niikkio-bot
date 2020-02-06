import logging
from bson.binary import Binary

import pymongo

from .base_writer import BaseWriter


class MongoWriter(BaseWriter):
    """Save files to MongoDB"""

    logger = logging.getLogger('niikkio').getChild('mongo')

    def __init__(self, category, connection_string):
        self.logger.debug('Connecting to mongo db...')
        self._client = pymongo.MongoClient(connection_string)
        self._db = self._client['niikkio-database']
        super().__init__(category)

    def save(self, user_id, source_filename):
        collection = self._db[self._category]
        with open(source_filename, 'rb') as f_in:
            encoded = Binary(f_in.read())
            doc = collection.find_one_and_update(
                {'uid': user_id},
                {'$push': {'entities': encoded}},
                projection=['uid'],
                upsert=True,
                return_document=pymongo.ReturnDocument.AFTER
            )

            self.logger.debug('Updating: ' + repr(doc))
