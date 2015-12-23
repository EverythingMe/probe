from probe.android.adb import adb

__author__ = 'rotem'


def get_version():
    float(adb.get_instance().shell('getprop ro.build.version.release').get('stdout')[0].strip())