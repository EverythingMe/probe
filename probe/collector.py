from __future__ import absolute_import
from .helpers.logger import logger
from .obj import classregistry
from .obj.output import CollectorOutput


class Collector(object):

    def __init__(self):
        pass

    def collect(self):
        collector_output = CollectorOutput()

        for measurer in classregistry.snapshot_registry:
            try:
                collector_output.add_measurement({measurer.name(): measurer.value()})
            except Exception as ex:
                logger.error('error collecting from {}. \n Exception details: {}'.format(measurer.__class__.__name__, ex.message))

            # reset measurer if needed for the next run
            reset = getattr(measurer, "reset", None)
            if callable(reset):
                measurer.reset()

        return collector_output