# Copyright (c) 2017 Thomas Karl Pietrowski

# Python built-ins
import os
import sys

# Uranium/Cura
from UM.Logger import Logger

# Using 3rd-party module directory
Logger.log("i", "Python version: {}".format(sys.version_info))
third_party_dir = os.path.join(os.path.split(__file__)[0], "..", "3rd-party")
if os.path.isdir(third_party_dir):
    Logger.log("d", "Found 3rd-party directory and adding in into PYTHONPATH.")
    sys.path.append(third_party_dir)

# win32* specific things
win32_dirs = [os.path.join(third_party_dir, "win32"),
              os.path.join(third_party_dir, "win32", "lib"),
              os.path.join(third_party_dir, "pywin32_system32"),
              ]
for win32_dir in win32_dirs:
    if os.path.isdir(win32_dir):
        sys.path.append(win32_dir)

# Trying to import one of the COM modules
try:
    from .PyWin32Connector import ComConnector
    Logger.log("i", "ComFactory: Using pywin32!")
except ImportError:
    from .ComTypesConnector import ComConnector
    Logger.logException("i", "ComFactory: Using comtypes!")