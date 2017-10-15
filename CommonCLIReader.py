# Copyright (c) 2017 Thomas Karl Pietrowski
from .CommonReader import CommonReader

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
    
    def exportFileAs(self, options):
        raise NotImplementedError("Exporting files is not implemented!")
    
    def read(self, file_path):
        options = self.readCommon(file_path)
        super().readOnSingleAppLayer(options)