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
    def __init__(self, data_dir='./data/video_validator', frames=10):
        self._frames = frames
        self._dir = os.path.abspath(data_dir)

        if platform.system() == 'Windows':
            self._dir = os.path.normpath(self._dir).replace('\\', '/')

    def check(self):

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