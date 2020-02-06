import os
import shutil
import logging
from .base_writer import BaseWriter

logger = logging.getLogger('niikkio')


class FileWriter(BaseWriter):
    def __init__(self, category, path):
        assert os.path.exists(path), 'PATH NOT EXISTS'
        self._path = path
        super().__init__(category)

    def save(self, user_id, source_filename):
        dest_dir = os.path.join(self._path, str(user_id))
        if not os.path.exists(dest_dir):
            os.mkdir(dest_dir)

        count = len(os.listdir(dest_dir))
        ext = os.path.splitext(source_filename)[1]

        dest_filename = f'{self._category}_message_{count}{ext}'

        logger.debug(f'Writing file to destination: {dest_filename}...')
        shutil.copyfile(source_filename, os.path.join(dest_dir, dest_filename))
