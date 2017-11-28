import os
import sys

# Using 3rd-party module directory
print("i", "Python version: {}".format(sys.version_info))
third_party_dir = os.path.join(os.path.split(__file__)[0], "..", "3rd-party")
if os.path.isdir(third_party_dir):
    print("d", "Found 3rd-party directory and adding in into PYTHONPATH.")
    sys.path.append(third_party_dir)

try:
    print("i", "Looking for win32com in Cura..")
    import win32com
    del win32com
except Exception as e:
    print("i", ".. Probably couldn't find it. Using our own..", str(e))
    # win32* specific things
    pyd_dirs = [os.path.join(third_party_dir, "pythonwin"),
                os.path.join(third_party_dir, "win32"),
                os.path.join(third_party_dir, "win32", "lib"),
                os.path.join(third_party_dir, "pywin32_system32"),
                ]
    for pyd_dir in pyd_dirs:
        pyd_dir = os.path.realpath(pyd_dir)
        if os.path.isdir(pyd_dir):
            sys.path.append(pyd_dir)
            print("i", "Added <{}> to sys.path!".format(pyd_dir))
    dll_dirs = [os.path.join(third_party_dir, "pywin32_system32"),
                ]
    for dll_dir in dll_dirs:
        dll_dir = os.path.realpath(dll_dir)
        if os.path.isdir(dll_dir):
            os.environ['PATH'] = dll_dir + ';' + os.environ['PATH']
            print("i", "Added <{}> to os.environ['PATH']!".format(dll_dir))
    
print("d", "sys.path: {}".format(sys.path))

# PyWin32 modules
import win32com
win32com.__gen_path__ = os.path.join(os.path.split(__file__)[0], "win32com_dir") 

import win32com.client
import pythoncom
import pywintypes

