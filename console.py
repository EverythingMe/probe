from __future__ import absolute_import
import click
import sys
from probe.android.adb import adb

from probe.probe import Probe
from probe.helpers.logger import logger, setup_logging
from probe.tricorder import Tricorder
from probe.measurers.probe import *
from probe.measurers.collector import *

# from time import sleep

__author__ = 'rotem'


@click.command()
@click.option('--package',      default='',                         help='Package name to run Probe on')
@click.option('--activity',     default='=',                        help='Activity to restart within that package')
@click.option('--apk-path',     default=None,                       help='Path to installed APK')
@click.option('--repeat-count', default=8,                          help='Times to repeat the test')
@click.option('--timeout',      default=15,                         help='probe will stop when logcat output is silent for that duration')
@click.option('--device-id',    default=None,                       help='device_id to send commands to')
def main(package, activity, repeat_count, apk_path, timeout, device_id):

    setup_logging()

    tricorder = Tricorder(package)
    adb.set_apk_path(apk_path)

    for x in range(repeat_count):
        # adb.logcat_clean()
        probe = Probe(tricorder, package, activity, device_id)
        logger.info('\ninstance no %s' % x)
        probe.start(timeout)

    normalized_result = tricorder.dump()
    previous_results = tricorder.get_previous_runs(normalized_result)

    # compare results with previous results (from db)
    build_successful, error_log = tricorder.compare_with_previous_results(previous_results, normalized_result)

    # Fail if results are above the defined threshold
    if build_successful:
        logger.info('Probe: run OK. All measurements from current in instance are within threshold bounds')
    else:
        logger.error('Probe: run failed! Summarizing failed tests:')
        logger.error('\n' + error_log)
    sys.exit(0 if build_successful else 1)

    # trico = Tricorder(package, 'test')
    # adb.logcat_clean()
    # probe = Probe(trico, package, activity, device_id)
    #
    # thread = Thread(target=probe.start)
    # thread.start()
    #
    # sleep(2)
    # probe.stop()




if __name__ == "__main__":
    main()