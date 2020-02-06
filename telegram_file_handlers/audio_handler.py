import logging
import os

import librosa

from .base_handler import BaseHandler


class AudioHandler(BaseHandler):
    """Audio files handler

    Before saving convert audio to .wav format with sample_rate = 16kHz
    """

    logger = logging.getLogger('niikkio').getChild('audio')

    @staticmethod
    def convert_to_wav(source_filename, dest_filename=None, sample_rate=16000):
        data, sr = librosa.load(source_filename, sr=sample_rate)
        if dest_filename is None:
            dest_filename = os.path.splitext(source_filename)[0] + '.wav'
        librosa.output.write_wav(dest_filename, data, sr)
        return dest_filename

    def handle(self, user_id, filename):
        self.logger.debug(f'Converting audio file to wav-format: {filename}...')
        wav_filename = AudioHandler.convert_to_wav(filename)

        self.logger.debug(f'Saving wav file: {wav_filename}...')
        self._save(user_id, wav_filename)
        os.remove(wav_filename)

        return 'Аудиосообщение обработано!'
