# native
import os
import platform
import atexit
import threading

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


# TODO: LAYOUT

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
            self.StartADBThread()
            self.adbThread.join()
            # TODO: make optional via config -> just set ADBHelper.pollStatus to false
            self.StartADBPollThread()

        startHidden = str(self.config['SETTINGS']['Start_Hidden'])
        if(startHidden.lower() == 'true'):
            self.GUI.onMinimizeToTray(None)
        self.StartWebThread()

    # For ADBHelper thread
    def StartADBHelper(self):
        self.ADBHelper = ADBHelper.ADBHelper(self)

    # ADBHelper thread launch by button
    def StartADBThread(self):
        self.adbThread = CustomThread.Thread(target=self.StartADBHelper)
        self.adbThread.start()

    # ADBHelper-Polling thread launch once by init
    # TODO: fix this mess... (╯°□°）╯︵ ┻━┻)
    def StartADBPollThread(self):
        self.adbPollThread = CustomThread.Thread(
            target=self.ADBHelper.PollDeviceWin)
        self.adbPollThread.start()

    def RestartADB(self):
        self.StopADB(True)
        self.StartADBThread()

    def StopADB(self, force):
        self.ADBHelper.OnExit()
        self.guiDict['ADB_Status'] = False
        self.guiDict['ADB_Tunnel'] = False
        self.guiDict['ConnectedDeviceName'] = '<none>'
        self.GUI.UpdateGUI()
        print("Stopping ADB Server...")
        if(force):
            if(self.adbThread.is_alive()):
                self.adbThread.terminate()

    # Webserver thread launch by init or button
    def StartWebThread(self):
        self.webThread = CustomThread.Thread(target=self.StartWebserver)
        self.webThread.daemon = True
        self.webThread.start()
        self.guiDict['Webserver_Status'] = True
        self.GUI.UpdateGUI()

    # Webserver thread restart by button
    def RestartWebserverThread(self):
        tmp = CustomThread.Thread(target=self.RestartWebserver)
        tmp.start()
        self.guiDict['Webserver_Status'] = False
        self.GUI.UpdateGUI()

    def onStopWebserver(self):
        self.server.stop()
        if(self.webThread.is_alive()):
            self.guiDict['Webserver_Status'] = False
            self.GUI.UpdateGUI()
            self.webThread.terminate()
        print("Webserver is stopping...")

    def RestartWebserver(self):
        self.server.stop()
        if(self.webThread.is_alive()):
            self.webThread.terminate()
        # TODO: Replace the whole sleeping everywhere with proper thread locking...
        time.sleep(3)
        if(not self.webThread.is_alive()):
            self.StartWebThread()
        else:
            print("Webserver couldn't be restarted. Check if port is alredy in use.")

    def StartWebserver(self):
        host = str(self.config['SETTINGS']['WebserverHost'])
        port = str(self.config['SETTINGS']['WebserverPort'])
        print("Webserver is starting on 'http://"+host+":"+port+"'...\n")
        self.server = Webserver.MyWSGIRefServer(host=host, port=port)
        self.wserver = Webserver.Webserver(server=self.server)
        self.wserver.start()

    # debug
    def SeeThreads(self):
        for obj in gc.get_objects():
            if isinstance(obj, Webserver.Webserver):
                print(obj.name)

    # called by GUIDrawer upon close
    def CleanExit(self):
        useADB = str(self.config['SETTINGS']['UseADB'])
        if(useADB.lower() == 'true'):
            # TODO: can't exit, when ADBThread isn't created yet. Find a way around that
            # self.ADBHelper.pollStatus = False
            pass


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
        'Start_Hidden': False,
        'Wait_For_Device': True,
        'ADBTunnelHostPort': 8000,
        'ADBTunnelClientPort': 8000,
        'WebserverHost': 'localhost',
        'WebserverPort': 8000
    }

    # Overwrites local config with file (if exists)
    config.read('config.ini')

    main = MainConnector(config)
