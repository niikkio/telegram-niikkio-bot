"""Convert audio file to .wav format"""
import argparse

from .audio_handler import AudioHandler

parser = argparse.ArgumentParser(
    description='Convert audio file to .wav format.', add_help=True)

required = parser.add_argument_group('required arguments')
required.add_argument('--source', help='source file', required=True)
required.add_argument('--dest', help='destination file', required=True)

args = parser.parse_args()

wav = AudioHandler.convert_to_wav(source_filename=args.source,
                                  dest_filename=args.dest)
print(f'Converted to {wav}!')
