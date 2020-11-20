import wx
import wx.adv
import os


class GUISystemtray(wx.adv.TaskBarIcon):

    def __init__(self,  parent):
        wx.adv.TaskBarIcon.__init__(self)

        self.parent = parent
        self.icon = wx.Icon()

        try:
            img = wx.Image(os.getcwd() + "/Assets/icon.png",
                           wx.BITMAP_TYPE_ANY)
            bmp = wx.Bitmap(img)
            self.icon.CopyFromBitmap(bmp)
        except:
            print("Icon not found, will use empty icon.")

        self.SetIcon(self.icon, "Android Control Server")
        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_DOWN, self.OnTaskBarRightClick)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarClick)

    def OnTaskBarClose(self, evt):
        self.parent.Close()

    def OnTaskBarClick(self, evt):
        self.parent.Show()
        self.parent.Restore()

    def OnTaskBarRightClick(self, evt):
        self.PopupMenu(TrayContextMenu(self))

    def OnMinimize(self, e):
        self.parent.onMinimizeToTray(None)

    def OnShow(self, e):
        self.OnTaskBarClick(None)

    def OnClose(self, e):
        self.parent.onClose(None)


class TrayContextMenu(wx.Menu):

    def __init__(self, parent):
        super(TrayContextMenu, self).__init__()

        self.parent = parent

        showT = wx.MenuItem(self, wx.NewId(), 'Show')
        self.Append(showT)
        self.Bind(wx.EVT_MENU, self.parent.OnShow, showT)

        minimizeT = wx.MenuItem(self, wx.NewId(), 'Minimize')
        self.Append(minimizeT)
        self.Bind(wx.EVT_MENU, self.parent.OnMinimize, minimizeT)

        closeT = wx.MenuItem(self, wx.NewId(), 'Close')
        self.Append(closeT)
        self.Bind(wx.EVT_MENU, self.parent.OnClose, closeT)

    def OnClose(self, e):
        self.parent.Close()

    def OnMinimize(self, e):
        self.parent.Iconize()
