from __future__ import absolute_import
import Queue
import threading
from probe.runtime import runtime

__author__ = 'rotem'


class AsyncLogcatReader(threading.Thread):
    """
    Helper class to implement asynchronous reading of a file
    in a separate thread. Pushes read lines on a queue to
    be consumed in another thread.
    """

    def __init__(self, process, queue, package_name):
        assert isinstance(queue, Queue.Queue)
        assert callable(process.stdout.readline)
        threading.Thread.__init__(self)
        self.daemon = True
        self._process = process
        self._fd = process.stdout
        self._queue = queue
        self._pid = runtime.get_pid()
        self._stop = threading.Event()

    def run(self):
        """
        The body of the thread: read lines and put them in the queue.
        """
        while not self.stopped():
            line = self._fd.readline()
            if self._pid in line:
                self._queue.put(line)
        self._fd.close()

    def eof(self):
        """
        Check whether there is no more content to expect.
        """
        return not self.is_alive() and self._queue.empty()

    def stop(self):
        self._stop.set()
        self._queue.put('\0')

    def stopped(self):
        return self._stop.isSet()