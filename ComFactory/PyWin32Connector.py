# Copyright (c) 2017 Thomas Karl Pietrowski

# PyWin32 modules
import win32com
win32com.__gen_path__ = os.path.join(os.path.split(__file__)[0], "win32com_dir") 

import win32com.client
import pythoncom
import pywintypes

class ComConnector:
    def CreateClassObject(app_name):
        return win32com.client.Dispatch(app_name)

    def CoInit():
        pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)

    def UnCoInit():
        pythoncom.CoUninitialize()

    def GetComObject(toBeObjected):
        return toBeObjected
    
    @property
    def IntByRef(self):
        return win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I1, 0)
