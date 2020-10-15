# native
import os
import platform
import threading
import configparser
import atexit

# pip packages
import wx

import Modules.GUIDrawer as GUIDrawer
import Modules.ADBHelper as ADBHelper


class MainConnector:
    def __init__(self, config):
        super(MainConnector, self)
        self.config = config

        # ADBHelper
        adbhelper = ADBHelper.ADBHelper(config)

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
    # Reads userconfig(config.ini) and passes it to ASCS obj
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'': ''}
    config.read('config.ini')

    main = MainConnector(config)
