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

    def write(self, user_id, src_filename):
        dst_dir = os.path.join(self._path, str(user_id))
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)

        count = len(os.listdir(dst_dir))
        ext = os.path.splitext(src_filename)[1]

        dst_filename = f'{self._category}_message_{count}{ext}'

        logger.debug(f'Writing file to destination: {dst_filename}...')
        shutil.copyfile(src_filename, os.path.join(dst_dir, dst_filename))

