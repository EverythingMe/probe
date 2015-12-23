__author__ = 'rotem'

continuous_registry = list()
snapshot_registry = list()


def register_continuous(measurer):
    continuous_registry.append(measurer)


def register_snapshot(measurer):
    snapshot_registry.append(measurer)