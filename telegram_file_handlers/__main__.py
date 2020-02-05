import sys
from .audio_handler import convert_to_wav
from .photo_handler import check_face

if len(sys.argv) == 3:
    if sys.argv[1] == '--convert':
        wav = convert_to_wav(sys.argv[2])
        print(f'Converted to {wav}!')

    if sys.argv[1] == '--check-face':
        face_cascade_source = 'config/haarcascade_frontalface_default.xml'
        eyes_cascade_source = 'config/haarcascade_eye.xml'
        result = check_face(sys.argv[2], face_cascade_source, eyes_cascade_source)
        print('Found face!' if result else 'Face not found!')
