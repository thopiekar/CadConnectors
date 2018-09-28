# Copyright (c) 2017 Thomas Karl Pietrowski

# Uranium
from UM.Platform import Platform # @UnresolvedImport
from UM.Logger import Logger # @UnresolvedImport

# CIU
from .CommonReader import CommonReader # @UnresolvedImport

# built-ins
import os
import subprocess

# OS dependent
if Platform.isWindows():
    import winreg

class CommonCLIReader(CommonReader):
    def __init__(self,
                 app_friendly_name):
        super().__init__(app_friendly_name)
        self._parallel_execution_allowed = True

    def preStartApp(self):
        # Nothing needs to be prepared before starting
        pass

    def startApp(self, options):
        # No start needed..
        return options

    def openForeignFile(self, options):
        # We open the file, while converting.. No actual opening of the file needed..
        return options

    def read(self, file_path):
        options = self.readCommon(file_path)
        result = super().readOnSingleAppLayer(options)

        # Unlock if needed
        if not self._parallel_execution_allowed:
            self.conversion_lock.release()

        return result

    def executeCommand(self, command, cwd = os.path.curdir, shell = None):
        if shell == None:
            if Platform.isWindows():
                shell = True
            else:
                shell = False

        environment_with_additional_path = os.environ.copy()
        if self._additional_paths:
            environment_with_additional_path["PATH"] = os.pathsep.join(self._additional_paths) + os.pathsep + environment_with_additional_path["PATH"]
        Logger.log("i", "Executing command: {}".format(command))
        p = subprocess.Popen(command,
                             cwd = cwd,
                             env = environment_with_additional_path,
                             shell = shell,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE,
                             )
        stdout, stderr = p.communicate()
        return p.returncode

    def scanForAllPaths(self):
        self._additional_paths = []
        if Platform.isWindows():
            for file_extension in self._supported_extensions:
                found_paths = self.findPathForExtensionAll(file_extension)
                if found_paths:
                    Logger.log("i", "Found path for {}: {}".format(file_extension, found_paths))
                    self._additional_paths += found_paths
        Logger.log("d", "The result is: \"{}\"".format(self._additional_paths))

    def findPathForExtensionAll(self, extension):
        paths = []
        for found_paths in (self.findPathForExtensionRootClassic(extension),
                            self.findPathForExtensionUserClassic(extension),
                            self.findPathForExtensionUserModern(extension),
                            ):
            if type(found_paths) is list:
                for path in found_paths:
                    if path not in paths:
                        paths.insert(0, path)
            elif found_paths is None:
                pass
            else:
                Logger.log("e", "Unknown data type for \"found_paths\": {}".format(type(found_paths)))
        return paths

    def findPathForExtensionUserModern(self, extension):
        key_base = winreg.HKEY_CURRENT_USER
        appid = None

        try:
            user_choice = winreg.OpenKey(key_base,
                                      os.path.join("Software",
                                                   "Microsoft",
                                                   "Windows",
                                                   "CurrentVersion",
                                                   "Explorer",
                                                   "FileExts",
                                                   extension,
                                                   "UserChoice"
                                                   ),
                                      )
            key_len = winreg.QueryInfoKey(user_choice)[1]
            for pos in range(key_len):
                entry = winreg.EnumValue(user_choice, pos)
                if entry[0].lower() == "ProgId".lower() and not appid:
                    appid = entry[1]
        except:
            Logger.logException("e", "Exception, while looking for AppID: \"{}\"".format(extension))
            return

        if appid:
            key_path = os.path.join("Software", "Classes", appid)

            result =  self._findPathForExtensionClassic(appid,
                                                        key_base,
                                                        key_path,
                                                        )
            Logger.log("d", "The result is: \"{}\"".format(result))
            return result

    def findPathForExtensionRootClassic(self, extension):
        key_base = winreg.HKEY_CLASSES_ROOT
        key_path = os.path.join("{}")

        result = self._findPathForExtensionClassic(extension,
                                                   key_base,
                                                   key_path,
                                                   )
        Logger.log("d", "The result is: \"{}\"".format(result))
        return result

    def findPathForExtensionUserClassic(self, extension):
        key_base = winreg.HKEY_CURRENT_USER
        key_path = os.path.join("Software", "Classes", "{}")

        result =  self._findPathForExtensionClassic(extension,
                                                    key_base,
                                                    key_path,
                                                    )
        Logger.log("d", "The result is: \"{}\"".format(result))
        return result

    def _findPathForExtensionClassic(self, extension, key_base, key_path):
        try:
            file_class = winreg.QueryValue(key_base,
                                           key_path.format(extension),
                                           )
        except FileNotFoundError as e:
            Logger.log("i", "File extension not found in registry: \"{}\"".format(extension))
            return
        except Exception as e:
            Logger.logException("e", "Unknown exception, while looking for extension: {}".format(extension))
            return

        if file_class and not file_class == extension:
            if not file_class == extension: # Otherwise we might end up in an endless loop
                Logger.log("d", "File extension seems to be an alias. Following \"{}\"...".format(file_class))
                result = self._findPathForExtensionClassic(file_class, key_base, key_path)

                if not result:
                    Logger.log("d", "Following \"{}\" gave no result. Trying to determine the command here...".format(file_class))
                else:
                    return result

        try:
            command = winreg.QueryValue(key_base, os.path.join(key_path.format(extension),
                                                               "shell",
                                                               "open",
                                                               "command"
                                                               ),
                                        )
        except FileNotFoundError as e:
            Logger.log("i", "File extension not found in registry: \"{}\"".format(extension))
            return
        except Exception as e:
            Logger.logException("e", "Unknown exception, while looking for the path of extension: {}".format(extension))
            return

        return self._convertCommandIntoPath(command)

    def _convertCommandIntoPath(self, command):
        try:
            splitted_command = command.split("\"")
            while "" in splitted_command:
                splitted_command.remove("")
            splitted_command = splitted_command[0]
            path = os.path.dirname(splitted_command)
        except Exception as e:
            Logger.logException("e", "Unknown exception, while formatting : <{}>".format(command))
            return

        if not os.path.isdir(path):
            return []
        else:
            return [path,]
