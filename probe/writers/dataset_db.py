from __future__ import absolute_import
import json
import os
import sys

import dataset

from .. import config
from ..helpers.logger import logger
from ..readers.readers import ProbeReader, CollectorReader


class Dataset(object):

    def __init__(self):
        self.db = None
        connection_string = os.getenv('PROBE_DB_CONNECTION_STRING', "sqlite:///mydatabase.db")
        try:
            logger.info('Trying to connect to db...'),
            self.db = dataset.connect(connection_string)
            logger.info('success')
        except Exception, e:
            print str(e)
            sys.exit(1)

    def read_json(self, prefix, reader):
        for file in os.listdir(config.JSON_OUTPUT_DIR):
            if file.endswith('.json') and file.startswith(prefix):
                logger.debug('Processing {}s'.format(file))
                file_path = os.path.join(config.JSON_OUTPUT_DIR, file)

                try:
                    json_data = open(file_path, 'r')
                    data = json.load(json_data)
                    json_data.close()
                    reader.write_to_table(data, self.db)
                except IOError as e:
                    logger.error(e)
                finally:
                    os.remove(file_path)

    def read_probe_json(self, test_name):
        probe_reader = ProbeReader(test_name)
        self.read_json('Probe', probe_reader)

    def read_collector_json(self, test_name):
        collector_reader = CollectorReader(test_name)
        self.read_json('Collector', collector_reader)

instance = Dataset()