# Copyright (c) 2017 Thomas Karl Pietrowski

# Uranium/Cura
from UM.Application import Application
from UM.i18n import i18nCatalog
i18n_catalog = i18nCatalog("CuraSolidWorksIntegrationPlugin")
from UM.Message import Message
from UM.Logger import Logger
from UM.Mesh.MeshReader import MeshReader
from UM.PluginRegistry import PluginRegistry
from UM.Scene.SceneNode import SceneNode

# Trying to import one of the COM modules
from .ComFactory import ComConnector
from .CommonReader import CommonReader

class CommonCOMReader(CommonReader):
    def __init__(self,
                 app_friendly_name,
                 app_com_service_family):
        CommonReader.__init__(self, app_friendly_name)
        self._default_app_name = app_com_service_family
        self._default_app_friendly_name = app_friendly_name
    
    @property
    def _app_names(self):
        return [self._default_app_name, ]
    
    def preStartApp(self):
        # Should get removed whenever possible
        pass
    
    def startApp(self, options):
        Logger.log("d", "Calling %s...", options["app_name"])
        try:
            try:
                options["app_instance"] = ComConnector.CreateActiveObject(options["app_name"])
                options["app_was_active"] = True
                options["app_started_with_coinit"] = False
            except:
                ComConnector.CoInit()
                options["app_instance"] = ComConnector.CreateActiveObject(options["app_name"])
                options["app_was_active"] = True
                options["app_started_with_coinit"] = True
        except:
            try:
                options["app_instance"] = ComConnector.CreateClassObject(options["app_name"])
                options["app_was_active"] = False
                options["app_started_with_coinit"] = False
            except:
                ComConnector.CoInit()
                options["app_instance"] = ComConnector.CreateClassObject(options["app_name"])
                options["app_was_active"] = False
                options["app_started_with_coinit"] = True
            

        return options
    
    def postCloseApp(self, options):
        # Coinit when inited
        if options["app_started_with_coinit"]:
            ComConnector.UnCoInit()
    
    def read(self, file_path):
        options = self.readCommon(file_path)
        if not self.preRead(options):
            Logger.log("d", "preRead failed..")
            return MeshReader.PreReadResult.cancelled
        return super().readOnMultipleAppLayer(options)
    
