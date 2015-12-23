from __future__ import absolute_import
from ...measurers.base import CpuTicks
from ...obj.meta import SnapshotRegistrar

__author__ = 'rotem'


class CpuTicksUser(CpuTicks):
    """
    Cpu usage user space (in ticks)
    """
    __metaclass__ = SnapshotRegistrar

    def __init__(self):
        pass

    def name(self):
        return 'cpu_ticks_user'

    def value(self):
        return super(self.__class__, self).value(13)


class CpuTicksKernel(CpuTicks):
    """
    Cpu usage kernel space(in ticks)
    """
    __metaclass__ = SnapshotRegistrar

    def __init__(self):
        pass

    def name(self):
        return 'cpu_ticks_kernel'

    def value(self):
        return super(self.__class__, self).value(14)
