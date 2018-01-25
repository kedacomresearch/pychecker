import subprocess
import time
import os
import json
import sys
import signal
import datetime
import platform
import shutil
import re
import logging


class Video_validator(object):
    def __init__(self, url, data_dir='./data/video_validator', frames=10):
        self._url = url
        self._frames = frames
        self._dir = os.path.abspath(data_dir)

        if platform.system() == 'Windows':
            self._dir = os.path.normpath(self._dir).replace('\\', '/')

    def capture(self):
        #clear data first
        if os.path.isdir(self._dir):
            shutil.rmtree(self._dir)
        os.makedirs(self._dir)
        gst_launch = 'gst-launch-1.0'
        if platform.system() == 'Windows':
            gst_launch += '.exe'

        proc = subprocess.Popen(
            [
                gst_launch,  #'-v' ,'-m',
                'rtspsrc',
                'location=%s' % self._url,
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
                'location={0}/%05d.jpg'.format(self._dir)
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)

        timeout = (2 + self._frames * 0.1) * 1000000
        base = datetime.datetime.now()

        filename = os.path.join(self._dir, '%05d.jpg' % (self._frames - 1))
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

    def recognize(self):

        config = os.path.join(self._dir, 'tesseract.config')
        f = open(config, 'w')
        f.write('tessedit_char_whitelist :0123456789-.')
        f.close()

        last = None

        for i in range(self._frames):

            filename = os.path.join(self._dir, '%05d.jpg' % i)
            resultfile = os.path.join(self._dir, '%05d' % i)
            proc = subprocess.Popen(
                ['tesseract.exe', filename, '-psm', '7', resultfile, config],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            #ret = proc.wait()
            while proc.poll() == None:
                pass
                # print proc.stdout.readline()

            if not (proc.returncode == 0):
                logging.error("ocr failed at No.%d frame!" % i)
                return False

            line = open(resultfile + '.txt', 'r').readline()

            pattern = re.compile(
                r'(?P<day>[0-9])\:(?P<hour>[0-9]{2})\:(?P<second>[0-9]{2})\.(?P<ms>[0-9]{3})'
            )
            m = pattern.match(line)

            if not m:
                logging.error('No.%d frame recognize not as expect <%s>' %
                              (i, line))
                return False

            ms = int(m.group('second')) * 1000 + int(m.group('ms'))

            if (last == None) or m == last + 100:
                continue
            else:
                logging.error(
                    'No.%d frame recognize timestamp (%d) not as expect (%d)' %
                    (i, m, last + 100))
                return False

        return True

    def check(self):
        return self.capture() and self.recognize()