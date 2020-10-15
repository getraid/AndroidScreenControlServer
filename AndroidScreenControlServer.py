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

        # ADBHelper
        adbhelper = ADBHelper.ADBHelper(self)

        windowThread = threading.Thread(target=self.StartGUI)
        windowThread.start()

    def StartGUI(self):
        # GUI
        app = wx.App()
        frm = GUIDrawer.GUIDrawer(
            self, None, title='Android Screen Control Server')
        frm.Show()
        app.MainLoop()


if __name__ == '__main__':
    # Reads userconfig(config.ini) and passes it to MainConnector obj
    config = configparser.ConfigParser()

    # Sets default config, if ini is missing
    config['SETTINGS'] = {
        'ADB_Platform_Tools_URL': 'https://dl.google.com/android/repository/platform-tools-latest-windows.zip'}

    # Overwrites local config with file (if exists)
    config.read('config.ini')

    main = MainConnector(config)
