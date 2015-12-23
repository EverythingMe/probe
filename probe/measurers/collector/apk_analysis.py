from __future__ import absolute_import
from ...runtime import runtime
from ...android.adb import adb
from ...obj.meta import SnapshotRegistrar

__author__ = 'rotem'


class ApkSize(object):
    __metaclass__ = SnapshotRegistrar
    def __init__(self):
        pass

    def name(self):
        return 'apk_size'

    def value(self):
        apk_size = adb.shell('ls -l data/app | grep {}'.format(runtime.get_package_name())).get('stdout')[0].split()[3]
        return int(apk_size)


class DexMethodCount(object):
    __metaclass__ = SnapshotRegistrar
    def __init__(self):
        self.method_count = 0

    def name(self):
        return 'apk_dex_method_count'

    def value(self):
        if self.method_count == 0:
            output = adb.exec_command('java -jar libs/dex-method-counts.jar {}'.format(adb.get_apk_path())).get('stdout')[2].split(':')[1].strip()
            self.method_count = int(output)

        return self.method_count