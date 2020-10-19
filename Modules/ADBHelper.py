# native
import os
import platform
import subprocess
import threading
import atexit
import sys
import socket

# pip packages
import configparser
import dload


class ADBHelper:
    """Mainly handles everything ADB (Android Debug Bridge) related"""

    def __init__(self, connector):
        super(ADBHelper, self)
        # register event on window close
        atexit.register(self.OnExit)
        # apply/set user configs
        self.connectorRef = connector
        # checks whether you run Windows, Linux or Mac and sets the commands accordingly
        self.StartADBServer()

    # Downloads newest version of ADB Plattform Tools for Windows
    def DownloadWin(self):
        # workaround when build as exe via pyinstaller
        if not os.path.exists("Modules"):
            os.system('mkdir Modules')
        url = str(
            self.connectorRef.config['SETTINGS']['ADB_Platform_Tools_URL'])
        print("Can not find platform-tools folder. Downloading from: " + url)
        dload.save_unzip(url, ".")

    # Searches in tasklist if adb.exe is there.
    # https://stackoverflow.com/a/29275361
    def __ProcessExistsWin(self, processName):
        call = 'TASKLIST', '/FI', 'imagename eq %s' % processName
        output = subprocess.check_output(call).decode()
        last_line = output.strip().split('\r\n')[-1]
        return last_line.lower().startswith(processName.lower())

    # If adb.exe couldn't be started, use this function.
    # Checks if adb.exe is running and adb port is opened
    def ADBRunningWin(self, stdoutTxt):
        output = False
        if not "daemon started successfully" in stdoutTxt:
            if self.__ProcessExistsWin('adb.exe'):
                print("Adb.exe is running from somewhere else. Checking port...")
            else:
                "Adb.exe is not running. Somewhere happend an error. Checking for port anyway..."
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', 5037))
            if result == 0:
                print("ADB server port is open")
                output = True
            else:
                print("ADB server port is closed...something went wrong.")
                output = False
            sock.close()
        else:
            output = True
        return output

    # Checks OS, downloads adb-tools and starts adb server
    def StartADBServer(self):
        if (platform.system() == "Windows"):
            # check if platform tools installed on win, else call DownloadADBWin.py
            if not os.path.exists("platform-tools"):
                self.DownloadWin()
            result = subprocess.getoutput(
                'platform-tools\\adb.exe start-server')
            # could slide a gui logger /logfile output in here, dunno yet
            print(result)
            checkADB = str(
                self.connectorRef.config['SETTINGS']['Dont_Check_For_ADBServer'])
            if (not checkADB.lower() == 'true'):
                self.connectorRef.guiDict['ADB_Status'] = self.ADBRunningWin(
                    result)

                # TODO: Use update instead of calling each time
                # https://stackoverflow.com/questions/14698631/wxpython-statictext-dynamic-update
                # self.connectorRef.GUI.st1.SetLabel(
                #     "Status ADB: " + str(self.connectorRef.guiDict['ADB_Status']))
                # self.connectorRef.guiDict["ConnectedDeviceName"] =  self.GetDeviceWin()
                # self.EstConnectionWin()
        # Linux and MacOs are planned, but I firstly want to focus on the Windows version
        # -------------------------------------------
        # # Linux
        # elif(platform.system() == "Linux"):
        #     print("tbd")
        # # MacOs
        # elif(platform.system() == "Darwin"):
        #     print("tbd")
        # else:
        #     print("err")

    def GetDeviceWin(self):
        result = subprocess.getoutput(
            'platform-tools\\adb.exe shell getprop ro.product.model')
        return print(result)

    def EstConnectionWin(self):
        os.system(
            'platform-tools\\adb.exe reverse tcp:8000 tcp:8000')
        pass

    # If window has been closed, kill adb server
    def OnExit(self):
        checkToString = str(
            self.connectorRef.config['SETTINGS']['Close_ADBServer_OnExit'])
        if(checkToString.lower() == 'true'):
            if platform.system() == "Windows":
                os.system('platform-tools\\adb.exe kill-server')
            else:
                os.system('adb kill-server')
            print("Stopped ADB Server.")
