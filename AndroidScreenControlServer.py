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
import gc


class MainConnector:
    """Connects every component together.
    Also starts GUI and other necessary sub-threads"""

    def __init__(self, config):
        super(MainConnector, self)
        self.config = config
        self.guiDict = {"ADB_Status": False,
                        "ConnectedDeviceName": '<none>', "ADB_Tunnel": False, 'Webserver_Status': False}

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

    # In this method other threads are started to update/start everything post gui creation
    def AfterGUIInit(self):
        self.GUI.UpdateGUI()
        afterGUIInitThread = CustomThread.Thread(
            target=self.AfterGUIInitThread)
        afterGUIInitThread.start()

    # Ensures that ADB is run first, to download necessary files
    def AfterGUIInitThread(self):
        useADB = str(self.config['SETTINGS']['UseADB'])
        if(useADB.lower() == 'true'):
            adbThread = CustomThread.Thread(target=self.StartADBHelper)
            adbThread.start()
            adbThread.join()
        self.StartWebThread()

    # For ADBHelper thread
    def StartADBHelper(self):
        self.ADBHelper = ADBHelper.ADBHelper(self)

    # ADBHelper thread launch by button
    def StartADBThread(self):
        self.adbThread = CustomThread.Thread(target=self.StartADBHelper)
        self.adbThread.start()

    def StartWebThread(self):
        self.webThread = CustomThread.Thread(target=self.StartWebserver)
        self.webThread.daemon = True
        self.webThread.start()

    def RestartWebserverThread(self):
        tmp = CustomThread.Thread(target=self.RestartWebserver)
        tmp.start()

    # TODO: Duplicate code. Needs refactor
    def RestartWebserver(self):
        self.server.stop()
        if(self.webThread.is_alive()):
            self.webThread.terminate()
        time.sleep(3)
        if(not self.webThread.is_alive()):
            self.StartWebThread()

    def SeeThreads(self):
        for obj in gc.get_objects():
            if isinstance(obj, Webserver.Webserver):
                print(obj.name)

    def StartWebserver(self):
        host = str(self.config['SETTINGS']['WebserverHost'])
        port = str(self.config['SETTINGS']['WebserverPort'])
        # TODO: define host & port in settings
        print("Webserver is starting on 'http://"+host+":"+port+"'...")
        self.server = Webserver.MyWSGIRefServer(host=host, port=port)
        self.wserver = Webserver.Webserver(server=self.server)
        self.wserver.start()


if __name__ == '__main__':
    # Reads userconfig(config.ini) and passes it to MainConnector obj
    config = configparser.ConfigParser()

    # Sets default config, if ini is missing
    config['SETTINGS'] = {
        'UseADB': True,
        'ADB_Platform_Tools_URL': 'https://dl.google.com/android/repository/platform-tools-latest-windows.zip',
        'Close_ADBServer_OnExit': True,
        'Dont_Check_For_ADBServer': False,
        'Start_Min_Sized': False,
        'Wait_For_Device': True,
        'ADBTunnelHostPort': 8000,
        'ADBTunnelClientPort': 8000,
        'WebserverHost': 'localhost',
        'WebserverPort': 8000
    }

    # Overwrites local config with file (if exists)
    config.read('config.ini')

    main = MainConnector(config)
