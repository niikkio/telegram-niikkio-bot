import logging
import cv2
import os
from .base_handler import BaseHandler

logger = logging.getLogger('niikkio').getChild('photo')


# noinspection PyUnresolvedReferences
class PhotoHandler(BaseHandler):
    def __init__(self, writers, face_cascade_source, eyes_cascade_source):
        assert os.path.exists(face_cascade_source), 'FACE_CASCADE NOT FOUND'
        assert os.path.exists(eyes_cascade_source), 'EYES_CASCADE NOT FOUND'
        # TODO: store classifier, not source
        self._face_cascade = cv2.CascadeClassifier(face_cascade_source)
        self._eyes_cascade = cv2.CascadeClassifier(eyes_cascade_source)
        super().__init__(writers)

    def check_face(self, filename):
        img = cv2.imread(filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = self._face_cascade.detectMultiScale(gray, 1.1, 4)
        eyes = self._eyes_cascade.detectMultiScale(gray, 1.1, 4)

        logger.debug(f'Found {len(faces)} faces and {len(eyes)} eyes')
        return len(faces) > 0 and len(eyes) > 0

    def handle(self, user_id, temp_filename):
        result = self.check_face(temp_filename)
        if result:
            logger.debug(f'Saving image: {temp_filename}...')
            self._save(user_id, temp_filename)
        else:
            logger.debug(f'Face not found: {temp_filename}')

        return 'Done!' if result else 'Face not found!'
