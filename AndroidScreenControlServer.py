# native
import os
import platform
import threading
import atexit

# pip packages
import wx
import configparser

# custom modules
import Modules.GUIDrawer as GUIDrawer
import Modules.ADBHelper as ADBHelper


class MainConnector:
    def __init__(self, config):
        super(MainConnector, self)
        self.config = config
        self.guiDict = {"ADB_Status": False}
        self.StartGUI()

    # Basic GUI settings and MainConnector.GUI creation
    def StartGUI(self):
        app = wx.App()
        frm = GUIDrawer.GUIDrawer(
            self, None, title='Android Screen Control Server')
        frm.Show()
        self.GUI = frm
        self.AfterGUIInit()
        app.MainLoop()

    # In this method other threads are started to update everything post gui creation
    def AfterGUIInit(self):
        # ADBHelper thread launch
        self.adbThread = threading.Thread(target=self.StartADBHelper)
        self.adbThread.start()

    # For ADBHelper thread
    def StartADBHelper(self):
        ADBHelper.ADBHelper(self)


if __name__ == '__main__':
    # Reads userconfig(config.ini) and passes it to MainConnector obj
    config = configparser.ConfigParser()

    # Sets default config, if ini is missing
    config['SETTINGS'] = {
        'ADB_Platform_Tools_URL': 'https://dl.google.com/android/repository/platform-tools-latest-windows.zip',
        'Close_ADBServer_OnExit': True,
        'Dont_Check_For_ADBServer': False
    }

    # Overwrites local config with file (if exists)
    config.read('config.ini')

    main = MainConnector(config)
