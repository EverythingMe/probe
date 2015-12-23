from __future__ import absolute_import
import Queue
import os
from subprocess import Popen, PIPE, STDOUT

from .android import adb
from .helpers.logger import logger
from .runtime import runtime
from .obj import classregistry
from .collector import Collector
from .android.logcat import AsyncLogcatReader
from .obj.output import ProbeOutput


__author__ = 'rotem'


class Probe():

    def __init__(self, tricorder, package, activity, device_id):
        self.stopped = False
        runtime.reset()
        runtime.package_name = package

        self.tricorder = tricorder
        self.adb = adb.adb
        self.adb.set_device_id(device_id)
        self.package_name = package
        self.probe_output = ProbeOutput()

        self.adb.kill(package)
        # cleanup logcat history before starting to collect log lines
        self.adb.logcat_clean()
        self.adb.start(package, activity)

        self.logcat = self.adb.logcat_start(package)
        self.stdout_queue = Queue.Queue()
        self.stdout_reader = AsyncLogcatReader(self.logcat, self.stdout_queue, self.package_name)

    def start(self, timeout=None):
        logger.debug('Probe listener started')
        logger.info('Listening on logcat output')
        self.stdout_reader.start()

        # Check the queues if we received some output (until there is nothing more to get).
        while not self.stdout_reader.eof() and not self.stopped:
            try:
                line = self.stdout_queue.get(timeout=timeout)
            except Queue.Empty:
                logger.info('%s\'s logcat output is silent for %d seconds, ' \
                      'considering that as steady state. Taking a snapshot with Collector now\n' % (self.package_name, timeout))
                break

            if line is None:
                break

            for measurer in classregistry.continuous_registry:
                if measurer.is_matching(line):
                    measurer.process(line)

        if not self.stopped:
            self.stop()

    def stop(self):
        self.stopped = True
        # Probe is the only consumer of stdout_reader, we can kill stdout_reader safely
        self.stdout_reader.stop()
        self.logcat.terminate()

        collector = Collector()
        collector_output = collector.collect()

        self.tricorder.record_probe(self.probe_output)
        self.tricorder.record_collector(collector_output)

        logger.info('Probe listener stopped {}'.format(self))

