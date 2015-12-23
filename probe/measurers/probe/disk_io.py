import re

from ...android.adb import adb
from ..base import LineCounter
from probe.obj.meta import GlobalRegistrar, SnapshotRegistrar


__author__ = 'rotem'

KB_READ_COLUMN = 4
KB_WRTN_COLUMN = 5


class IOStat(object):

    __metaclass__ = SnapshotRegistrar

    def __init__(self):
        self.reset()

    def measure_iostat(self):
        kb_read = 0
        kb_wrtn = 0
        iostat_list = adb.shell('iostat -k').get('stdout')
        relevant = False

        for line in iostat_list:
            line = line.strip().split()

            if relevant and len(line) == KB_WRTN_COLUMN+1:
                kb_read += int(line[KB_READ_COLUMN])
                kb_wrtn += int(line[KB_WRTN_COLUMN])

            if len(line) > 0 and line[0] == 'Device:':
                relevant = True

        return [kb_read, kb_wrtn]

    def name(self):
        return 'iostat'

    def value(self):
        kb_read_end, kb_wrtn_end = self.measure_iostat()
        self.kb_read = kb_read_end - self.kb_read
        self.kb_wrtn = kb_wrtn_end - self.kb_wrtn
        return {'kb_read': self.kb_read, 'kb_wrtn': self.kb_wrtn}

    def reset(self):
        self.kb_read, self.kb_wrtn = self.measure_iostat()
