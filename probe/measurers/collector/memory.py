from __future__ import absolute_import
from ...measurers.base import DumpsysMeminfo
from ...obj.meta import SnapshotRegistrar

__author__ = 'rotem'


class DalvikHeap(DumpsysMeminfo):

    __metaclass__ = SnapshotRegistrar

    def name(self):
        return 'dalvik_heap'

    def value(self):
        return super(self.__class__, self).value('Dalvik Heap', 7)


class NativeHeap(DumpsysMeminfo):

    __metaclass__ = SnapshotRegistrar

    def name(self):
        return 'native_heap'

    def value(self):
        return super(self.__class__, self).value('Native Heap', 7)


class PssTotal(DumpsysMeminfo):

    __metaclass__ = SnapshotRegistrar

    def name(self):
        return 'pss_total'

    def value(self):
        return super(self.__class__, self).value('TOTAL', 1)