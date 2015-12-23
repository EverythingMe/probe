import importlib
import pkgutil

__author__ = 'rotem'

l = [name for _, name, _ in pkgutil.iter_modules(__path__)]
# print 'XXX:', __file__,__name__, l
for name in l:
    importlib.import_module('.{}'.format(name), package=__name__)
