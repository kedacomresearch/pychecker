# from video_validator import Video_validator
from audio_validator import Audio_validator
import os
import platform
import argparse

# python pycheker.py --audio test.wav --freq 5000 --energy 0.99

if __name__ == '__main__':
    # test environment
    tesseractd = os.environ.get('TESSDATA_PREFIX')
    assert tesseractd, 'You may not install tesseract-ocr or its data files'
    sep = ':'
    if platform.system() == 'Windows':
        sep = ';'
    os.environ['PATH'] = tesseractd + sep + os.environ['PATH']

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a',
        '--audio',
        default='',
        help='enable audio check and set test file')
    parser.add_argument(
        '--freq', type=int, default=2000, help='audio target frequency (Hz)')
    parser.add_argument(
        '-b',
        '--band-width',
        type=int,
        default=1000,
        help=
        'frequecy band width to test, if target frequecy is 5000Hz, band width is 1000Hz, it\'ll check the energy percent of 4500Hz ~ 5500Hz'
    )
    parser.add_argument(
        '-e',
        '--energy',
        type=float,
        default=0.9,
        help='energy percent',
    )
    args = parser.parse_args()
    print args
    if not args.audio == '':
        rc = Audio_validator(args.audio)
        print rc.check(args.freq, args.band_width, args.energy)
