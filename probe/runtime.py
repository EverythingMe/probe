from __future__ import absolute_import
from .android.adb import adb

__author__ = 'rotem'

class Runtime():
    ''''''
    def __init__(self):
        self.package_name = None
        self.version_name = None
        self.version_code = None
        self.pid = None

    def get_package_name(self):
        return self.package_name

    def get_version_name(self):
        if not self.version_name:
            self.version_name = adb.version_name_cleaned(self.package_name)
        return self.version_name

    def get_version_code(self):
        if not self.version_code:
            self.version_code = adb.version_code(self.package_name)
        return self.version_code

    def get_pid(self):
        if not self.pid:
            self.pid = adb.get_pid(self.package_name)
        return self.pid

    def reset(self):
        self.package_name = None
        self.version_name = None
        self.version_code = None
        self.pid = None

runtime = Runtime()