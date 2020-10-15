import os
import platform
import threading
import configparser
import atexit
import dload
import sys


class ADBHelper:
    def __init__(self, config):
        super(ADBHelper, self)
        # register event on window close
        atexit.register(self.OnExit)
        # apply/set user configs
        self.config = config
        self.ApplyConfig()
        # call class main function
        self.CheckVer()

    def OnExit(self):
        if platform.system() == "Windows":
            os.system('platform-tools\\adb.exe kill-server')
        else:
            os.system('adb kill-server')

    def Download(self):
        print(sys.path)
        dload.save_unzip(
            "https://dl.google.com/android/repository/platform-tools-latest-windows.zip", ".")

    def ApplyConfig(self):
        pass

    def CheckVer(self):
        if (platform.system() == "Windows"):
            # check if platform tools installed on win, else call DownloadADBWin.py
            os.system('platform-tools\\adb.exe usb')
            if not os.path.exists("platform-tools"):
                self.Download()
            # init install subroutine

        # MacOs
        elif(platform.system() == "Darwin"):
            # init install subroutine
            print("tbd")
        else:
            print("err")
