from __future__ import absolute_import
from ..runtime import runtime
from ..android.adb import adb
from ..helpers.logger import logger

__author__ = 'rotem'


class LineCounter(object):

    def __init__(self):
        self.reset()

    def process(self, line):
        # logger.debug('{}: {}'.format(self.__class__.__name__, line))
        self.matching_lines += 1

    def value(self):
        return self.matching_lines

    def reset(self):
        self.matching_lines = 0


class DumpsysMeminfo(object):

    def __init__(self):
        pass

    def value(self, key, index):
        package_name = runtime.get_package_name()
        value = adb.shell('dumpsys meminfo {} | grep "{}"'.format(package_name, key)).get('stdout')[0].split()[index]
        return int(value)


class CpuTicks(object):

    def __init__(self):
        pass

    def value(self, index):
        pid = runtime.get_pid()
        procstat = adb.shell('cat /proc/{}/stat'.format(pid))['stdout'][0].split()
        return int(procstat[index])