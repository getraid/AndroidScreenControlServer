# native
import os
import platform
import atexit

# pip packages
import wx
import configparser

# custom modules
import Modules.CustomThread as CustomThread
import Modules.GUIDrawer as GUIDrawer
import Modules.ADBHelper as ADBHelper
import Modules.Webserver as Webserver
import time


class MainConnector:
    """Connects every component together.
    Also starts GUI and other necessary sub-threads"""

    def __init__(self, config):
        super(MainConnector, self)
        self.config = config
        self.guiDict = {"ADB_Status": False, "ConnectedDeviceName": ''}

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
        self.adbThread = CustomThread.Thread(target=self.StartADBHelper)
        self.webThread = CustomThread.Thread(target=self.StartWebserver)
        self.webThread.daemon = True

        self.adbThread.start()
        self.webThread.start()

        # time.sleep(5)
        # self.webThread.terminate()

    # For ADBHelper thread

    def StartADBHelper(self):
        self.ADBHelper = ADBHelper.ADBHelper(self)

    # For ADBHelper thread
    def StartWebserver(self):
        # TODO: define host & port in settings
        print("Webserver is starting on 'http://localhost:8091'...")
        self.server = Webserver.Webserver(host='localhost', port=8091)
        self.server.start()


if __name__ == '__main__':
    # Reads userconfig(config.ini) and passes it to MainConnector obj
    config = configparser.ConfigParser()

    # Sets default config, if ini is missing
    config['SETTINGS'] = {
        'ADB_Platform_Tools_URL': 'https://dl.google.com/android/repository/platform-tools-latest-windows.zip',
        'Close_ADBServer_OnExit': True,
        'Dont_Check_For_ADBServer': False,
        'Start_Min_Sized': False
    }

    # Overwrites local config with file (if exists)
    config.read('config.ini')

    main = MainConnector(config)
