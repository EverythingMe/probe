from __future__ import absolute_import
from ...runtime import runtime
from ...android.adb import adb
from ...obj.meta import SnapshotRegistrar
# from ...helpers.logger import logger
# import pprint
__author__ = 'rotem'


class SizeOnDisk(object):
    __metaclass__ = SnapshotRegistrar
    def __init__(self):
        pass

    def name(self):
        return 'size_on_disk'

    def value(self):
        apk_size = adb.shell('du -s /data/data/{}'.format(runtime.get_package_name())).get('stdout')[0].split()[0]

        # logger.debug(pprint.pprint(map(str.strip, adb.shell('du /data/data/{}'.format(runtime.get_package_name())).get('stdout'))))
        return int(apk_size) * 1024