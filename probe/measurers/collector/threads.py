from __future__ import absolute_import
from ...runtime import runtime
from ...android.adb import adb
from ...obj.meta import SnapshotRegistrar

__author__ = 'joey'


class NumThreads(object):
    __metaclass__ = SnapshotRegistrar
    def __init__(self):
        pass

    def name(self):
        return 'num_of_threads'

    def value(self):
        num_threads = adb.shell('top -n 1 | grep %s' % runtime.get_package_name()).get('stdout')[0].split()[4]
        return int(num_threads)