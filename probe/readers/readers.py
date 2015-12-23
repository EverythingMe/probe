from abc import ABCMeta, abstractmethod
import datetime

__author__ = 'rotem'


class Reader(object):
    __metaclass__ = ABCMeta

    # @abstractmethod
    # def read_json(self):
    #     pass

    @abstractmethod
    def write_to_table(self, data, db):
        pass


class CollectorReader(Reader):

    def __init__(self, test_name=None):
        self.flattened = dict()
        self.test_name = test_name

    def write_to_table(self, data, db):
        table = db['collector{}'.format(('_' + self.test_name) if self.test_name else '')]
        flattened = self.flatten(data)
        flattened['created_at'] = datetime.datetime.now()

        try:
            table.insert(flattened)
            db.commit()
        except Exception:
            db.rollback()

    # faltten the given data, preparing it to be stored in a db
    def flatten(self, data):

        for key in data:
            if isinstance(data[key], dict):
                self.flatten(data[key])
            else:
                self.flattened[key] = data[key]

        return self.flattened


class ProbeReader(Reader):

    def __init__(self, test_name=None):
        self.test_name = test_name

    def write_to_table(self, data, db):
        table = db['probe{}'.format(('_' + self.test_name) if self.test_name else '')]
        created_at = datetime.datetime.now()

        try:
            for key in data['timestamped_heapsize']:
                table.insert(dict(  build_number=data['build_number'],
                                    version_code=data['version_code'],
                                    timestamp=key['timestamp'],
                                    heapsize=key['heapsize'],
                                    allocated=key['allocated'],
                                    created_at=created_at))
            db.commit()
        except Exception:
            db.rollback()