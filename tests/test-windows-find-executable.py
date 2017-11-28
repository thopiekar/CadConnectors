# Copyright (c) 2017 Thomas Karl Pietrowski

import winreg
import os

file_class = winreg.QueryValue(winreg.HKEY_CLASSES_ROOT, ".FCStd".lower())
file_class = winreg.QueryValue(winreg.HKEY_CLASSES_ROOT, os.path.join(file_class,"shell", "open", "command"))
file_class = file_class.split("\"")
while "" in file_class:
    file_class.remove("")
file_class = file_class[0]
path, executable = os.path.split(file_class)
print(path)