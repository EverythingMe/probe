import time
import datetime

from ...helpers.logger import logger
from ...obj.meta import GlobalRegistrar


__author__ = 'rotem'


class GcForAllocLine(object):

    __metaclass__ = GlobalRegistrar

    def __init__(self):
        self.reset()

    def name(self):
        return 'gc_stats'

    def is_matching(self, line):
        return 'GC_FOR_ALLOC' in line

    def process(self, line):
        timestamped_heapsize = TimestampedHeapSize(extract_timestamp(line), 
                                                   extract_gc_for_alloc_heap_allocated(line),
                                                   extract_gc_for_alloc_heap_size(line))
        self.lines.append(timestamped_heapsize)

        # normalize timestamp with the first item as 0
        if self.first_timestamp is 0:
            self.first_timestamp = timestamped_heapsize.timestamp

        timestamped_heapsize.timestamp -= self.first_timestamp

        logger.debug('GC_FOR_ALLOC line: %s' % timestamped_heapsize.__dict__)

    def value(self):
        gc_count = len(self.lines)
        return {'gc_for_alloc': gc_count}

    def reset(self):
        self.first_timestamp = 0
        self.lines = list()


def extract_timestamp(line):
    timestamp = line[line.find(' '): line.find('.') + 3]
    return timestamp


# extracts current allocated heap from GC_FOR_ALLOC lines.
def extract_gc_for_alloc_heap_allocated(line):
    return int(line[(line.find('free ') + 5): line.find('K/')].strip())


# extracts current heap size from GC_FOR_ALLOC lines.
def extract_gc_for_alloc_heap_size(line):
    return int(line[(line.rfind('/')+1): line.rfind('K')].strip())


class TimestampedHeapSize(object):
    """
    save each heapsize with the current timestamp
    """
    def __init__(self, timestamp, allocated, heapsize):
        positive_unix_timestamp = '%s:%s' % ('2014', timestamp)
        parsed = datetime.datetime.strptime(positive_unix_timestamp,'%Y: %H:%M:%S.%f')

        self.timestamp = int(time.mktime(parsed.timetuple())*1e3 + parsed.microsecond/1e3)
        self.allocated = allocated
        self.heapsize = heapsize