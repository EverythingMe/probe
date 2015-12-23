# import importlib
# import pkgutil
#
# __author__ = 'rotem'
#
# modules = [name for _, name, _ in pkgutil.iter_modules(__path__)]
# print 'XXX:', __path__,__file__,__name__, modules
# for name in modules:
#     sub_path = __path__
#     sub_path[0] += name
#     modules = [subname for _, name, _ in pkgutil.iter_modules(sub_path)]
#         if modules = None
#         importlib.import_module('.{}'.format(name), package=__path__)
