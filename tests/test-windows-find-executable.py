# Copyright (c) 2017 Thomas Karl Pietrowski

import winreg
import os


class Test():
    def _findPathFromExtension(self, extension):
        try:
            file_class = winreg.QueryValue(winreg.HKEY_CLASSES_ROOT, extension)
            file_class = winreg.QueryValue(winreg.HKEY_CLASSES_ROOT, os.path.join(file_class,
                                                                                  "shell",
                                                                                  "open",
                                                                                  "command",
                                                                                  )
                                           )
            file_class = file_class.split("\"")
            while "" in file_class:
                file_class.remove("")
            file_class = file_class[0]
            path = os.path.split(file_class)[0]
            if os.path.isdir(path):
                return path
        except:
            print("e", "Could not find PATH for extension: {}".format(extension))
        return


t = Test()
p = t._findPathFromExtension(".FCStd".lower())
print(p)