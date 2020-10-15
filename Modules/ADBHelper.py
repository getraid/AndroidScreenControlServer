# native
import os
import platform
import threading
import atexit
import sys

# pip packages
import configparser
import dload


class ADBHelper:
    def __init__(self, connector):
        super(ADBHelper, self)
        # register event on window close
        atexit.register(self.OnExit)
        # apply/set user configs
        self.connectorRef = connector
        # checks whether you run Windows, Linux or Mac and sets the commands accordingly
        self.CheckVer()

    def Download(self):
        # workaround when build as exe via pyinstaller
        os.system('mkdir modules')
        url = str(
            self.connectorRef.config['SETTINGS']['ADB_Platform_Tools_URL'])
        print("Can not find platform-tools folder. Downloading from: " + url)
        dload.save_unzip(url, ".")

    def CheckVer(self):
        if (platform.system() == "Windows"):
            # check if platform tools installed on win, else call DownloadADBWin.py
            os.system('platform-tools\\adb.exe usb')
            if not os.path.exists("platform-tools"):
                self.Download()
        # Linux and MacOs are planned, but I firstly want to focus on the Windows version
        # -------------------------------------------
        # # Linux
        # elif(platform.system() == "Linux"):
        #     # init install subroutine
        #     print("tbd")
        # # MacOs
        # elif(platform.system() == "Darwin"):
        #     # init install subroutine
        #     print("tbd")
        # else:
        #     print("err")

    def OnExit(self):
        if platform.system() == "Windows":
            os.system('platform-tools\\adb.exe kill-server')
        else:
            os.system('adb kill-server')
