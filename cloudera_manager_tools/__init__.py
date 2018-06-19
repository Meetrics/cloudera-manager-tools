# Create a different scope (function) for the module init process, not to expose imports, temp variables, etc
def _init():
  from os import listdir
  from os.path import dirname, basename, join

  # TODO: move services/modules in a subfolder
  
  return [basename(f)[:-3] for f in listdir(dirname(__file__)) if f[-3:] == '.py' and not f.startswith('__')]

# __all__ defines what to export when import "*" is used
__all__ = _init()


# Import __all__ by default
from cloudera_manager_tools import *


# Clean up module init env
del _init
