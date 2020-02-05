from abc import abstractmethod
import os
import requests
import shutil


def generate_tmp_filename(file_path):
    return str(abs(hash(file_path))) + os.path.splitext(file_path)[1]


class BaseHandler:
    def __init__(self, url, writers=None):
        self._url = url
        self._writers = writers

    def _save(self, user_id, tmp_filename):
        if self._writers is not None:
            for w in self._writers:
                w.write(user_id, tmp_filename)

        os.remove(tmp_filename)

    def _download(self, file_path):
        download_url = f'{self._url}/{file_path}'

        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
            # TODO: use tempfile
            tmp_filename = generate_tmp_filename(file_path)
            with open(tmp_filename, 'wb') as f_out:
                shutil.copyfileobj(response.raw, f_out)

            return tmp_filename

    @abstractmethod
    def handle(self, user_id, file_path):
        """process entity"""
