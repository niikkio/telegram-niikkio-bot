import sys
from .audio_handler import convert_to_wav

if len(sys.argv) == 3:
    if sys.argv[1] == '--convert':
        wav = convert_to_wav(sys.argv[2])
        print(f'Converted to {wav}!')
