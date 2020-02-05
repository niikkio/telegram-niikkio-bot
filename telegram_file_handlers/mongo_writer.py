import pymongo
from bson.binary import Binary
import logging
from .base_writer import BaseWriter

logger = logging.getLogger('niikkio').getChild('mongo')


class MongoWriter(BaseWriter):
    def __init__(self, category, connection_string):
        logger.debug('Connecting to mongo db...')
        logger.debug(f'connection_string={connection_string}')
        self._client = pymongo.MongoClient(connection_string)
        self._db = self._client['niikkio-database']
        super().__init__(category)

    def write(self, user_id, src_filename):
        collection = self._db[self._category]
        with open(src_filename, 'rb') as f_in:
            encoded = Binary(f_in.read())
            doc = collection.find_one_and_update(
                {'uid': user_id},
                {'$push': {'entities': encoded}},
                projection={'uid': True, '_id': True, 'entities': False},
                upsert=True,
                return_document=pymongo.ReturnDocument.AFTER
            )

            logger.debug('Updating: ' + repr(doc))
