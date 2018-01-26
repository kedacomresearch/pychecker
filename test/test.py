# ocr = RTSPClientOCR('rtsp://127.0.0.1:8554/test')
# assert ocr.check()

import subprocess
import time
import platform
import os
import shutil
import datetime
import logging
import pychecker.media as pychecker


def capture(url, data_dir='./data/video_validator', frames=10):
    #clear data first
    if os.path.isdir(data_dir):
        shutil.rmtree(data_dir)
    os.makedirs(data_dir)
    gst_launch = 'gst-launch-1.0'
    if platform.system() == 'Windows':
        gst_launch += '.exe'

    proc = subprocess.Popen(
        [
            gst_launch,  #'-v' ,'-m',
            'rtspsrc',
            'location=%s' % url,
            '!',
            'rtph264depay',
            '!',
            'h264parse',
            '!',
            'capsfilter',
            'caps="video/x-h264,width=320,height=240,framerate=(fraction)10/1"',
            '!',
            'avdec_h264',
            '!',
            'jpegenc',
            '!',
            'multifilesink',
            'location={0}/%05d.jpg'.format(data_dir)
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)

    timeout = (2 + frames * 0.1) * 1000000
    base = datetime.datetime.now()

    filename = os.path.join(data_dir, '%05d.jpg' % (frames - 1))
    while True:
        passed = datetime.datetime.now() - base
        ms = passed.seconds * 1000 + passed.microseconds
        if ms > timeout:
            logging.error('%s Timeout')
            proc.kill()
            return False
        if os.path.isfile(filename):
            proc.kill()
            return True
    proc.kill()


if __name__ == '__main__':

    gst_launch = 'gst-launch-1.0'
    if platform.system() == 'Windows':
        gst_launch += '.exe'

    rtsp_server = subprocess.Popen(
        [
            'wsf-gstreamer-rtsptestserver', '"videotestsrc  pattern=3 \
        ! video/x-raw,width=320,height=240,framerate=10/1 \
        ! timeoverlay color=4278190080 draw-shadow=false draw-outline=false font-desc=\"Arial, 48\" \
        ! x264enc ! rtph264pay name=pay0 pt=96"'
        ],
        stdin=subprocess.PIPE)

    capture('rtsp://127.0.0.1:8554/test')
    if pychecker.video_check():
        print 'video test OK!'
    else:
        print 'video test failed!'

    rtsp_server.communicate("q")
    count = 0
    while rtsp_server.poll() == None:
        time.sleep(0.1)
        count += 1
        if count >= 10:
            rtsp_server.kill()
        assert count < 10, "wsf-gstreamer-rtsptestserver not exit in 1 second "

    command = [
        gst_launch,  #'-v' ,'-m',
        'audiotestsrc',
        'freq=5000',
        'num-buffers=500',
        '!',
        'wavenc',
        '!',
        'filesink',
        'location=test.wav'
    ]

    proc = subprocess.Popen(
        command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    while proc.poll() == None:
        time.sleep(0.1)
    if pychecker.audio_check('src\\test.wav'):
        print 'audio test OK!'
    else:
        print 'audio test failed!'
