from __future__ import absolute_import
from ..runtime import runtime


class CollectorOutput(object):

    def __init__(self, measurements=None, test_name=None):

        if not measurements:
            self.measurements = dict()
        else:
            self.measurements = measurements

        self.build_number = runtime.get_version_name()
        self.version_code = runtime.get_version_code()
        self.test_name = test_name

    def add_measurement(self, measurement):
        self.measurements.update(measurement)


class ProbeOutput(object):

    def __init__(self):
        self.timestamped_heapsize = []
        self.build_number = runtime.get_version_name()
        self.version_code = runtime.get_version_code()
