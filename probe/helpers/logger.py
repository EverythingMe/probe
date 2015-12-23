import logging
import pprint

__author__ = 'rotem'


logger = logging.getLogger('probe')


def setup_logging():
    formatter = logging.Formatter('%(levelname)s:(Probe): %(message)s')
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    file_handler_debug = logging.FileHandler('probe-debug.log')
    file_handler_debug.setLevel(logging.DEBUG)
    file_handler_debug.setFormatter(formatter)
    logger.addHandler(file_handler_debug)
    file_handler_brief = logging.FileHandler('probe-brief.log')
    file_handler_brief.setLevel(logging.INFO)
    file_handler_brief.setFormatter(formatter)
    logger.addHandler(file_handler_brief)


class PrettyLog():
    def __init__(self, obj):
        self.obj = obj
    def __repr__(self):
        return pprint.pformat(self.obj)