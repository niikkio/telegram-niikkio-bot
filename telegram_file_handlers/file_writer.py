import logging
import os
import shutil

from .base_writer import BaseWriter


class FileWriter(BaseWriter):
    """Save files to filesystem"""

    logger = logging.getLogger('niikkio')

    def __init__(self, category, path):
        self._path = path
        super().__init__(category)

    def save(self, user_id, source_filename):
        dest_dir = os.path.join(self._path, str(user_id))
        if not os.path.exists(dest_dir):
            os.mkdir(dest_dir)

        # Generate unique filename:
        count = len(os.listdir(dest_dir))  # count files in target directory
        ext = os.path.splitext(source_filename)[1]  # get file extension

        dest_filename = f'{self._category}_message_{count}{ext}'

        self.logger.debug(f'Writing file to destination: {dest_filename}...')
        shutil.copyfile(source_filename, os.path.join(dest_dir, dest_filename))
