import logging

import cv2

from .base_handler import BaseHandler


# noinspection PyUnresolvedReferences
class PhotoHandler(BaseHandler):
    """Photo file handler

    Save only photos with human face detected
    """

    logger = logging.getLogger('niikkio').getChild('photo')

    def __init__(self, writers, face_cascade_source, eyes_cascade_source):
        # Loading cascades:
        self._face_cascade = cv2.CascadeClassifier(face_cascade_source)
        self._eyes_cascade = cv2.CascadeClassifier(eyes_cascade_source)
        super().__init__(writers)

    def find_face(self, filename):
        img = cv2.imread(filename)  # Read the input image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

        # Detect faces and eyes:
        faces = self._face_cascade.detectMultiScale(gray, 1.1, 4)
        eyes = self._eyes_cascade.detectMultiScale(gray, 1.1, 4)

        self.logger.debug(f'Found {len(faces)} faces and {len(eyes)} eyes')
        return len(faces) > 0 and len(eyes) > 0

    def handle(self, user_id, filename):
        if self.find_face(filename):
            self.logger.debug(f'Saving image: {filename}...')
            self._save(user_id, filename)
            return 'Фотография сохранена!'
        else:
            self.logger.debug(f'Face not found: {filename}')
            return 'Лицо не обнаружено, фотография не будет сохранена'
