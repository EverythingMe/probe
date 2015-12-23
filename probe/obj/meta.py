from __future__ import absolute_import
from ..helpers.logger import logger
from ..obj import classregistry

__author__ = 'rotem'


class Registrar(type):

    def __new__(self, name, bases, attrs):

        if name.startswith('None'):
            return None

        # Go over attributes and see if they should be renamed.
        newattrs = {}
        for attrname, attrvalue in attrs.iteritems():
            if getattr(attrvalue, 'is_hook', 0):
                newattrs['__%s__' % attrname] = attrvalue
            else:
                newattrs[attrname] = attrvalue

        return super(Registrar, self).__new__(self, name, bases, newattrs)

    def __init__(cls, name, bases, attrs):
        super(Registrar, cls).__init__(name, bases, attrs)

        cls.register()

    def register(self):
        pass


class ContinuousRegistrar(Registrar):
    def register(self):
        # print ("registering class %s as a %s" % (self.__name__, self.__metaclass__.__name__))
        logger.info("registering class %s as a %s" % (self.__name__, self.__metaclass__.__name__))
        measurer = self()
        classregistry.register_continuous(measurer)


class SnapshotRegistrar(Registrar):
    def register(self):
        # print ("registering class %s as a %s" % (self.__name__, self.__metaclass__.__name__))
        logger.info("registering class %s as a %s" % (self.__name__, self.__metaclass__.__name__))
        measurer = self()
        classregistry.register_snapshot(measurer)


class GlobalRegistrar(Registrar):
    def register(self):
        # print ("registering class %s as a %s" % (self.__name__, self.__metaclass__.__name__))
        logger.info('registering class %s as a %s' % (self.__name__, self.__metaclass__.__name__))
        measurer = self()
        classregistry.register_snapshot(measurer)
        classregistry.register_continuous(measurer)