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

# custom pip package (read README.md)
from ppadb.client import Client as AdbClient


class ADBHelper:
    """Mainly handles everything ADB (Android Debug Bridge) related"""

    def __init__(self, connector):
        super(ADBHelper, self)
        # register event on window close
        atexit.register(self.OnExit)

        # ADB Client init, server gets downloaded with 'DownloadWin' and 'config.ini'
        self.client = AdbClient(host="127.0.0.1", port=5037)

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
        # throws error without sleep...?
        time.sleep(1)
        print("Can not find platform-tools folder.Downloading...\n")
        dload.save_unzip(url, ".")
        print("Download completed.")

    # Searches in tasklist if adb.exe is there.
    # https://stackoverflow.com/a/29275361
    def __ProcessExistsWin(self, processName):
        try:
            call = 'TASKLIST', '/FI', 'imagename eq %s' % processName
            output = subprocess.check_output(call).decode()
            last_line = output.strip().split('\r\n')[-1]
            return last_line.lower().startswith(processName.lower())
        except:
            return None

    # If adb.exe couldn't be started, use this function.
    # Checks if adb.exe is running and adb port is opened

    def ADBRunningWin(self, stdoutTxt):
        output = False
        tmp = self.CheckSocket(True) == 0
        if not "daemon started successfully" in stdoutTxt:
            if self.__ProcessExistsWin('adb.exe'):
                print("Adb.exe is running from somewhere else. Checking port...")
                output = True
            else:
                print(
                    "Adb.exe is not running. Somewhere happend an error. Checking for port anyway...")
                output = tmp
        else:
            output = tmp

        return output

    def CheckSocket(self, init):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 5037))
        if result == 0:
            print("ADB server port is open")
            output = True
        else:
            if(init):
                print("ADB server port is closed...something went wrong.")
            output = False
        sock.close()
        return result

    # Checks OS, downloads adb-tools and starts adb server
    def StartADBServer(self):
        if (platform.system() == "Windows"):
            # check if platform tools installed on win, else call DownloadADBWin.py
            if not os.path.exists("platform-tools"):
                self.DownloadWin()
            result = subprocess.getoutput(
                'platform-tools\\adb.exe start-server')
            print(result)
            checkADB = str(
                self.connectorRef.config['SETTINGS']['Dont_Check_For_ADBServer'])
            if (not checkADB.lower() == 'true'):
                self.connectorRef.guiDict['ADB_Status'] = self.ADBRunningWin(
                    result)
                self.connectorRef.GUI.UpdateGUI()
                self.WaitForDeviceWin()
                self.connectorRef.guiDict['ConnectedDeviceName'] = self.GetDeviceNames(
                )
                self.connectorRef.guiDict['ADB_Tunnel'] = self.EstConnection(str(self.connectorRef.config['SETTINGS']['ADBTunnelClientPort']),
                                                                             str(self.connectorRef.config['SETTINGS']['ADBTunnelHostPort']))

                self.connectorRef.GUI.UpdateGUI()

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

    # TODO: now useless function, will remove later
    def WaitForDeviceWin(self):
        print("Connect your android device with ADB developer usb settings enabled now.")
        # os.system('platform-tools\\adb.exe wait-for-device')

    def GetDeviceNames(self):
        result = ''
        dev = self.client.devices()
        for i in range(0, len(dev)):
            rip = dev[i].get_properties()
            result += (rip['ro.product.manufacturer'] +
                       ' ' + rip['ro.product.model'])
            if(not (i == len(dev)-1)):
                result += ', '
        print(result)
        if(result == ''):
            result = '<none>'
        return result

    def EstConnection(self, portHost, portDevice):
        result = ''
        if(len(self.client.devices()) <= 0):
            result = 'No Device connected - Please connect a device and restart ADB Server'
        else:
            for item in self.client.devices():
                item.reverse("tcp:"+portHost, "tcp:"+portDevice)

        if(result == ''):
            print("ADB Tunnel established")
            return True
        else:
            print(result)
            return False

    def RemoveConnection(self):
        result = ''
        if(len(self.client.devices()) <= 0):
            result = 'No Device connected - Please restart ADB Server'
        else:
            for item in self.client.devices():
                item.remove_reverse_all()

        if(result == ''):
            print("All ADB Tunnels cleared")
            return True
        else:
            print(result)
            return False

    # If window has been closed, kill adb server
    def OnExit(self):
        checkToString = str(
            self.connectorRef.config['SETTINGS']['Close_ADBServer_OnExit'])
        if(checkToString.lower() == 'true'):
            # TODO: Check if already process already killed in removeconnection
            if(self.CheckSocket(False) == 0):
                self.RemoveConnection()
                self.client.kill()
