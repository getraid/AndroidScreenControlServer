import os
import platform
import wx

if (platform.system() == "Windows"):
    # check if platform tools installed on win, else call DownloadADBWin.py
    os.system('platform-tools\\adb.exe usb')
elif(platform.system() == "Linux"):
    # init install subroutine
    os.system('adb usb')
# MacOs
elif(platform.system() == "Darwin"):
    # init install subroutine
    print("tbd")
else:
    print("err")


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
