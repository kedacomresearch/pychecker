from video_validator import Video_validator
from audio_validator import Audio_validator

# import os
# import platform
# import argparse

# python pycheker.py --audio test.wav --freq 5000 --energy 0.99

# if __name__ == '__main__':
#     # test environment
#     tesseractd = os.environ.get('TESSDATA_PREFIX')
#     assert tesseractd, 'You may not install tesseract-ocr or its data files'
#     sep = ':'
#     if platform.system() == 'Windows':
#         sep = ';'
#     os.environ['PATH'] = tesseractd + sep + os.environ['PATH']

#     # parse arguments
#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         '--video', default='', help='enable video check and set test url')
#     # parser.add_argument(
#     #     '--frames', type=int, default=10, help='video frames to test')

#     parser.add_argument(
#         '--audio', default='', help='enable audio check and set test file')
#     parser.add_argument(
#         '--freq', type=int, default=2000, help='audio target frequency (Hz)')
#     parser.add_argument(
#         '--band-width',
#         type=int,
#         default=1000,
#         help=
#         'frequecy band width to test, if target frequecy is 5000Hz, band width is 1000Hz, it\'ll check the energy percent of 4500Hz ~ 5500Hz'
#     )
#     parser.add_argument(
#         '--energy',
#         type=float,
#         default=0.9,
#         help='energy percent',
#     )
#     args = parser.parse_args()
#     print args
# if not args.video == '':
#     video = Video_validator(args.video)
#     video_rc = video.check()
#     print video_rc


# if not args.audio == '':
#     audio = Audio_validator(args.audio)
#     audio_rc = audio.check(args.freq, args.band_width, args.energy)
#     print audio_rc
def video_check(data_dir='./data/video_validator', frames=10):
    video = Video_validator(data_dir, frames)
    video_rc = video.check()
    # print video_rc
    return video_rc


def audio_check(file, freq=5000, band_width=1000, energy=0.9):
    audio = Audio_validator(file)
    audio_rc = audio.check(freq, band_width, energy)
    # print audio_rc
    return audio_rc


__all__ = ['video_check', 'audio_check']
