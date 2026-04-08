#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# A simple text-based progress bar, compatible with the basic API of:
# https://github.com/WoLpH/python-progressbar
#
# Copyright (C) 2021  Red Hat, Inc.
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# USA.


import shutil
import sys
import time


class ProgressBar:
    FORMAT = '{value:>10} / {max_value:<10} [{bars}]'
    BARS = '= '
    SPINLEN = 5

    def __init__(self, stream=sys.stderr, max_width=80, fps=10):
        self._stream = stream
        self._max_width = max_width
        self._min_delay = 1 / fps

    @staticmethod
    def _format_value(value):
        raise NotImplementedError()

    def start(self, max_value):
        self._value = 0
        self._max_value = max_value or 0
        self._status = dict()
        self._spinner = 0
        self._timestamp = 0
        self.update(0)

    def update(self, value):
        self._value = value
        if value > self._max_value:
            self._max_value = 0

        ts = time.time()
        if (ts - self._timestamp) < self._min_delay:
            return
        self._timestamp = ts

        status = {'value': self._format_value(value),
                  'max_value': self._format_value(self._max_value) \
                               if self._max_value else '???',
                  'bars': ''}

        termw = min(shutil.get_terminal_size()[0], self._max_width)
        nbars = max(termw - len(self.FORMAT.format(**status)), 0)
        nfill = nskip = 0

        if self._max_value:
            nfill = round(nbars * value / self._max_value)
        elif nbars > self.SPINLEN:
            nfill = self.SPINLEN
            nskip = self._spinner % (nbars - self.SPINLEN)
            self._spinner = nskip + 1

        status['bars'] = self.BARS[1] * nskip + \
                         self.BARS[0] * nfill + \
                         self.BARS[1] * (nbars - nfill - nskip)

        if status == self._status:
            return
        self._status = status

        self._stream.write('\r')
        self._stream.write(self.FORMAT.format(**self._status))
        self._stream.flush()

    def finish(self):
        self._max_value = self._value
        self._timestamp = 0  # Force an update
        self.update(self._value)

        self._stream.write('\n')
        self._stream.flush()


class DataTransferBar(ProgressBar):
    @staticmethod
    def _format_value(value):
        symbols = ' KMGTPEZY'
        depth = 0
        max_depth = len(symbols) - 1
        unit = 1024.0

        # 1023.95 should be formatted as 1.0 (not 1024.0)
        # More info: https://stackoverflow.com/a/63839503
        thres = unit - 0.05

        while value >= thres and depth < max_depth:
            depth += 1
            value /= unit
        symbol = ' %siB' % symbols[depth] if depth > 0 else ''

        return '%.1f%s' % (value, symbol)


if __name__ == '__main__':
    # Show a dummy bar for debugging purposes

    bar = DataTransferBar()
    size = 50*1024*1024
    chunk = 1024*1234
    recvd = 0

    bar.start(size)
    while recvd < (size - chunk):
        recvd += chunk
        bar.update(recvd)
        time.sleep(0.1)
    bar.update(size)
    bar.finish()
