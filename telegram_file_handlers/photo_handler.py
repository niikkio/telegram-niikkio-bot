import logging
import cv2
import os
from .base_handler import BaseHandler

logger = logging.getLogger('niikkio').getChild('photo')


# noinspection PyUnresolvedReferences
def check_face(filename, face_cascade_source, eyes_cascade_source):
    face_cascade = cv2.CascadeClassifier(face_cascade_source)
    eyes_cascade = cv2.CascadeClassifier(eyes_cascade_source)

    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    eyes = eyes_cascade.detectMultiScale(gray, 1.1, 4)

    logger.debug(f'Found {len(faces)} faces and {len(eyes)} eyes')
    return len(faces) > 0 and len(eyes) > 0


class PhotoHandler(BaseHandler):
    def __init__(self, *args, face_cascade_source, eyes_cascade_source):
        assert os.path.exists(face_cascade_source), 'FACE_CASCADE NOT FOUND'
        assert os.path.exists(eyes_cascade_source), 'EYES_CASCADE NOT FOUND'
        # TODO: store classifier, not source
        self._face_cascade_source = face_cascade_source
        self._eyes_cascade_source = eyes_cascade_source
        super().__init__(*args)

    def handle(self, user_id, file_path):
        logger.debug(f'Downloading file: {file_path}...')
        tmp_filename = self._download(file_path)

        result = check_face(tmp_filename, self._face_cascade_source, self._eyes_cascade_source)
        if result:
            logger.debug(f'Saving image: {tmp_filename}...')
            self._save(user_id, tmp_filename)
        else:
            logger.debug(f'Face not found: {tmp_filename}')

        os.remove(tmp_filename)
        return 'Done!' if result else 'Face not found!'
