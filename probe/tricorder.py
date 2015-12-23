from __future__ import absolute_import

from .parser import jsonparser

from .helpers.logger import logger
from probe.helpers import numbers
from probe.helpers.logger import PrettyLog
from .runtime import runtime
from .writers import dataset_db
from .android.adb import Adb
from .obj.output import CollectorOutput


__author__ = 'rotem'


class Tricorder():
    GRACE_FACTOR = 1.1

    def __init__(self, package_name, test_name=None):
        self.package_name = package_name
        self.test_name = test_name
        self.adb = Adb()

        self.probe_instances = list()
        self.collector_instances = list()

    def record_probe(self, probe_output):
        self.probe_instances.append(probe_output)

    def record_collector(self, collector_output):
        collector_output.measurements = self.flatten(collector_output.measurements)
        self.collector_instances.append(collector_output)

    def flatten(self, data, prefix=None):
        for k, v in data.items():
            del data[k]
            if isinstance(v, dict):
                flattened = self.flatten(v, k)
                data.update(flattened)
            elif v is not None:
                key = '_'.join(filter(None, (prefix, k)))
                data[key] = v

        return data

    def normalize_output(self):

        logger.debug('Normalizing output from %s instances' % len(self.collector_instances))
        instances = list()
        for instance in self.collector_instances:
            instances.append(instance.measurements)
        aggregated = self.aggregate_results(instances)

        normalized_mean_result = dict()

        # calculate statistics and remove anomalies (everything outside one std from mean)
        for key, value in aggregated.iteritems():
            measurements = aggregated[key]
            std = numbers.pstdev(measurements)
            mean = numbers.get_mean(measurements)

            logger.debug('Evaluating std for \'{}\': '
                        'mean: {}, std: {}, measurements: {}'.format(key, mean, std, measurements))
            for measurement in measurements:
                if numbers.is_out_of_bounds(measurement, mean, std):
                    aggregated[key].remove(measurement)
                    logger.debug('\'{}\': {} is more than one std ({}) from the mean ({}), '
                                'removing from measurements'.format(key, measurement, std, mean))

                normalized_mean_result[key] = numbers.get_mean(aggregated[key])

        logger.debug('Normalized result: %s' % PrettyLog(normalized_mean_result))
        return normalized_mean_result

    def compare_with_previous_results(self, outputs_list, end_result):
        """Compare results with previous runs"""
        test_successful = True
        error_log = ''
        logger.debug('Probe: calculating previous runs statistics, will fail this run if an anomaly is found, '
                    'Grace factor is: {}'.format(self.GRACE_FACTOR))
        logger.debug('================================================================================\n')

        aggregated = self.aggregate_results(outputs_list)

        # calculate statistics and fail build if an anomaly was found (everything outside one std from mean)
        for key, value in aggregated.iteritems():
            measurements = aggregated[key]
            # skip empty results
            if not measurements:
                logger.debug("Empty aggregated results for {}, skipping!".format(measurements))
                continue

            std = numbers.pstdev(measurements)
            mean = numbers.get_mean(measurements)

            logger.debug('Evaluating std for \'{}\': '
                        'mean: {}, std: {}, previous results: {}'.format(key, "%.2f" % mean, "%.2f" % std,
                                                                         measurements))

            if key in end_result:
                measurement = end_result[key]
                if numbers.is_out_of_upper_bound(measurement, mean * self.GRACE_FACTOR, std):
                    error = '--> Run failed: \'{}\': {} is more than one std ({}) from the mean ({})'.format(key,
                                                                                                             measurement,
                                                                                                             "%.2f" % std,
                                                                                                             "%.2f" % mean)
                    error_log += error + '\n'
                    logger.error(error)
                    test_successful = False

        logger.debug('================================================================================\n')
        return test_successful, error_log

    def aggregate_results(self, results):
        """ create an aggregated result which includes measured key -> list of results from all instances """
        aggregated = dict()
        for instance in results:
            for key, value in instance.iteritems():

                if not isinstance(value, (int, long, float, complex, type(None))):
                    logger.error('{key} ({value}) is not a number, can not add it, dropping {key}'.format(key=key, value=value))
                    continue

                if not aggregated.get(key):
                    aggregated[key] = list()
                if value is not None:
                    aggregated[key].append(value)

        return aggregated

    def dump(self):
        """Dump normalized data to jsons, and then to DB (deleteing the succesfully uploaded jsons)"""
        normalized_collector_dump = self.normalize_output()
        collector_output = CollectorOutput(normalized_collector_dump, self.test_name)

        logger.debug('Dumping normalized data')
        jsonparser.gen_json('Collector', self.test_name, self.package_name, collector_output)

        i = 0
        for probe_instance in self.probe_instances:
            probe_instance.build_number = '{}-{}'.format(runtime.get_version_name(), i)
            jsonparser.gen_json('Probe', self.test_name, self.package_name, probe_instance)
            i += 1

        ds_writer = dataset_db.instance
        ds_writer.read_probe_json(self.test_name)
        ds_writer.read_collector_json(self.test_name)

        return normalized_collector_dump

    def get_previous_runs(self, end_result):
        """Get previous results from db"""
        result_keys = set(end_result.keys())

        ds_writer = dataset_db.instance
        response = ds_writer.db.query("SELECT * FROM {table} p \
                                        JOIN ((SELECT Build_number, max(Created_at) as max_time \
                                        FROM {table} \
                                        GROUP BY Build_number)) m ON (p.Build_number=m.Build_number and p.created_at=m.max_time) \
                                        ORDER BY p.Build_number desc \
                                        LIMIT 10".format(table='collector{}'.format('_'+self.test_name if self.test_name else '')))

        aggregated_prev_results = list()
        for row in response:
            for row_key in row:
                if not row_key in result_keys:
                    del row[row_key]

            aggregated_prev_results.append(row)

        return aggregated_prev_results