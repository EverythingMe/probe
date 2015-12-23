from __future__ import absolute_import
from multiprocessing import TimeoutError
import os
from subprocess import Popen, PIPE, STDOUT
import sys
from time import sleep

from ..helpers.logger import logger
from ..helpers.timeout import Timeout


class Adb:
    device_id = None
    apk_path = None

    def __init__(self):
        self.adb_path = os.path.join(os.environ['ANDROID_HOME'], 'platform-tools/adb')

    def set_device_id(self, device_id):
        self.device_id = device_id

    def set_apk_path(self, apk_path):
        self.apk_path = apk_path

    def get_apk_path(self):
        if not self.apk_path:
            logger.error('apk path not set, use --apk-path option in command line options')
        return self.apk_path

    def exec_command(self, cmd):
        # logger.debug(cmd)
        results = dict()
        cmd_res = Popen(cmd, stdout=PIPE, shell=True)

        cmd_res.wait()
        results['stdout'] = cmd_res.stdout.readlines()
        results['pid'] = cmd_res.pid

        return results

    def base_adb_cmd_string(self, adb_cmd):
        return '{adb_path} {device_id} {adb_cmd}'.format(adb_path=self.adb_path,
                                                        device_id='-s {0}'.format(self.device_id) if self.device_id else '',
                                                        adb_cmd=adb_cmd)
    def adb(self, adb_cmd):

        return self.exec_command(self.base_adb_cmd_string(adb_cmd))

    def pull(self, remote, local=''):
        return self.adb('pull {} {}'.format(remote, local))
        # os.system(cmd)

    def shell(self, adb_cmd):
        return self.adb('shell {}'.format(adb_cmd))

    def kill(self, package_name):
        return self.shell('am force-stop {}'.format(package_name))

    def start(self, package_name, activity_name):
        return self.shell('am start {}/{}'.format(package_name, activity_name))

    def logcat(self, params):
        cmd = self.base_adb_cmd_string('logcat {}'.format(params))
        logcat = Popen(os.path.expanduser(cmd).split(), stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=False)
        # grep = Popen(['grep',  self.get_pid(package)], stdout=PIPE, stdin=logcat.stdout, stderr=STDOUT, shell=False)

        return logcat

    def logcat_start(self, package):
        return self.logcat('-v threadtime')

    def logcat_clean(self):
        return self.adb('logcat -c')

    def version_code(self, package):
        reply = self.shell('dumpsys package %s | grep versionCode=' % package)
        if not reply:
            report_no_package(package)

        reply = reply.get('stdout')[0].split('=')[1].strip()
        return int(reply.split()[0])

    def version_name(self, package):
        reply = self.shell('dumpsys package %s | grep versionName=' % package)
        if not reply or not reply.get('stdout'):
            report_no_package(package)

        reply = reply.get('stdout')[0].split('=')[1].strip()
        return reply

    def version_name_cleaned(self, package):
        version_name = self.version_name(package)

        return version_name.split('-')[0]

    def get_pid(self, package):
        cmd = 'ps | grep %s' % package

        logger.info('trying to resolve pid for {}.'.format(package)),
        try:
            with Timeout(seconds=10):
                while True:
                    pids = self.shell(cmd)['stdout']
                    for line in pids:
                        #looks for the pid of the main process, child processes (':') are filtered
                        if package in line and ':' and '/' not in line:
                            uid_and_pid = line.strip().split(' ')
                            pid = filter(None, uid_and_pid)
                            logger.info('success')
                            return pid[1]
                    logger.info("."),
                    sleep(0.1)
        except TimeoutError:
            # couldn't find package, report and exit
            report_no_package(package)


def report_no_package(package):
    logger.error('can\'t find {}, is it installed?'.format(package))
    sys.exit(1)

adb = Adb()