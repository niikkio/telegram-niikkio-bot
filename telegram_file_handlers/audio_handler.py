import logging
# TODO: suppress 'UserWarning: PySoundFile failed. Trying audioread instead.'
import librosa
import os
from .base_handler import BaseHandler

logger = logging.getLogger('niikkio').getChild('audio')


def convert_to_wav(src_filename, sample_rate=16000):
    data, sr = librosa.load(src_filename, sr=sample_rate)
    dst_filename = os.path.splitext(src_filename)[0] + '.wav'
    librosa.output.write_wav(dst_filename, data, sr)
    return dst_filename


class AudioHandler(BaseHandler):
    def handle(self, user_id, file_path):
        logger.debug(f'Downloading file: {file_path}...')
        tmp_filename = self._download(file_path)

        logger.debug(f'Converting audio file to wav-format: {tmp_filename}...')
        wav_filename = convert_to_wav(tmp_filename)
        os.remove(tmp_filename)

        logger.debug(f'Saving wav file: {wav_filename}...')
        self._save(user_id, wav_filename)
