import logging
# TODO: suppress 'UserWarning: PySoundFile failed. Trying audioread instead.'
import librosa
import os
from .base_handler import BaseHandler

logger = logging.getLogger('niikkio').getChild('audio')


class AudioHandler(BaseHandler):
    @staticmethod
    def convert_to_wav(source_filename, dest_filename=None, sample_rate=16000):
        data, sr = librosa.load(source_filename, sr=sample_rate)
        if dest_filename is None:
            dest_filename = os.path.splitext(source_filename)[0] + '.wav'
        librosa.output.write_wav(dest_filename, data, sr)
        return dest_filename

    def handle(self, user_id, temp_filename):
        logger.debug(f'Converting audio file to wav-format: {temp_filename}...')
        wav_filename = AudioHandler.convert_to_wav(temp_filename)

        logger.debug(f'Saving wav file: {wav_filename}...')
        self._save(user_id, wav_filename)
        os.remove(wav_filename)

        return 'Done!'
