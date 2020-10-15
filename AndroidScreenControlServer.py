# native
import os
import platform
import threading
import configparser
import atexit

# pip packages
import wx

# submodules
import Modules.DownloadADBWin as DownloadADBWin


class ASCS:
    def __init__(self, config):
        super(ASCS, self)
        atexit.register(self.OnExit)
        self.config = config
        self.ApplyConfig()
        self.main()

    def OnExit(self):
        if platform.system() == "Windows":
            os.system('platform-tools\\adb.exe kill-server')
        else:
            os.system('adb kill-server')

    def ApplyConfig(self):
        pass

    def CheckVer(self):
        if (platform.system() == "Windows"):
            # check if platform tools installed on win, else call DownloadADBWin.py
            os.system('platform-tools\\adb.exe usb')
            if not os.path.exists("platform-tools"):
                DownloadADBWin.Download()
            # init install subroutine

        # MacOs
        elif(platform.system() == "Darwin"):
            # init install subroutine
            print("tbd")
        else:
            print("err")

    def DrawGUI(self):
        a = wx.App()
        window = wx.Frame(None, title="Android Screen Control Server")
        # create a panel in the frame
        pnl = wx.Panel(window)
        # put some text with a larger bold font on it
        st = wx.StaticText(pnl, label="debug")
        font = st.GetFont()
        font.PointSize += 10
        font = font.Bold()
        st.SetFont(font)

        window.Show()
        a.MainLoop()

    def main(self):
        print(self.config['DEFAULT']['HideWindow'])
        self.CheckVer()
        windowThread = threading.Thread(target=self.DrawGUI(), args=(1,))
        windowThread.start()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'HideWindow': 'false'}

    config.read('config.ini')

    ascs = ASCS(config)
