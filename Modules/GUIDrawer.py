# native
import atexit
# pip packages
import wx
import wx.adv
import sys
import Modules.GUISystemtray as GUISystemtray
import os

# Mostly generated with wxGlade


class GUIDrawer(wx.Frame):
    """Draws GUI ...obviously"""

    def __init__(self, connector, *args, **kw):
        # ensure the parent's __init__ is called
        super(GUIDrawer, self).__init__(*args, **kw)

        # VARS
        self.connectorRef = connector

        # METHODS
        self.InitializeWindow(**kw)

    def InitializeWindow(self, **kw):

        kw["style"] = kw.get("style", 0) | wx.DEFAULT_FRAME_STYLE

        icon = wx.Icon()
        try:
            icon.CopyFromBitmap(
                wx.Bitmap(os.getcwd() + "/Assets/icon.png", wx.BITMAP_TYPE_ANY))
        except:
            print("Icon not found, will use empty icon.")

        self.SetIcon(icon)

        # If setting of Start_Min_Sized true, window will start up in a small size
        sizeOpt = str(self.connectorRef.config['SETTINGS']['Start_Min_Sized'])
        if (sizeOpt.lower() == 'true'):
            self.SetSize((370, 250))
        else:
            self.SetSize((700, 400))

        self.SetMinSize((370, 250))
        self.frame_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        item = wxglade_tmp_menu.Append(
            wx.ID_ANY, "Restart Webserver", "Restarts the included webserver")
        self.Bind(wx.EVT_MENU, self.onRestartWebserver, id=item.GetId())
        wxglade_tmp_menu.AppendSeparator()
        item = wxglade_tmp_menu.Append(
            wx.ID_ANY, "Restart ADB", "Restarts ADB Server")
        self.Bind(wx.EVT_MENU, self.onRestartADB, id=item.GetId())
        # item = wxglade_tmp_menu.Append(
        #     wx.ID_ANY, "Reconnect ADB Port", "Creates internal reverse proxy through USB")
        # self.Bind(wx.EVT_MENU, self.onRestartADBPort, id=item.GetId())
        item = wxglade_tmp_menu.Append(
            wx.ID_ANY, "Stop ADB", "Stops ADB Server")
        self.Bind(wx.EVT_MENU, self.onStopADB, id=item.GetId())
        wxglade_tmp_menu.AppendSeparator()
        item = wxglade_tmp_menu.Append(
            wx.ID_ANY, "Minimize to Tray", "Minimizes window to system tray")
        self.Bind(wx.EVT_MENU, self.onMinimizeToTray, id=item.GetId())
        item = wxglade_tmp_menu.Append(
            wx.ID_ANY, "Exit", "Stops all servers and closes the program.")
        self.Bind(wx.EVT_MENU, self.onExitCmd, id=item.GetId())
        self.frame_menubar.Append(wxglade_tmp_menu, "Quick Options")
        self.SetMenuBar(self.frame_menubar)
        # Menu Bar end
        self.Tabs = wx.Notebook(self, wx.ID_ANY)
        self.StartPane = wx.Panel(self.Tabs, wx.ID_ANY)
        self.Logger = wx.TextCtrl(
            self.StartPane, wx.ID_ANY, "", style=wx.HSCROLL | wx.TE_MULTILINE | wx.TE_READONLY)
        self.ServerCtrl = wx.Panel(self.Tabs, wx.ID_ANY)
        self.restartWebSrvBtn = wx.Button(
            self.ServerCtrl, wx.ID_ANY, "Restart Webserver")
        self.stopWebSrvBtn = wx.Button(
            self.ServerCtrl, wx.ID_ANY, "Stop Webserver")
        self.startWebSrvBtn = wx.Button(
            self.ServerCtrl, wx.ID_ANY, "Start Webserver")
        self.restartAdbBtn = wx.Button(
            self.ServerCtrl, wx.ID_ANY, "Restart ADB")
        self.stopAdbBtn = wx.Button(self.ServerCtrl, wx.ID_ANY, "Stop ADB")
        self.startAdbBtn = wx.Button(self.ServerCtrl, wx.ID_ANY, "Start ADB")
        # self.restartAdbTunnelBtn = wx.Button(
        #     self.ServerCtrl, wx.ID_ANY, "Restart ADB Tunnel")
        self.reloadPluginsBtn = wx.Button(
            self.ServerCtrl, wx.ID_ANY, "Reload Plugins")
        self.minimizeToTrayBtn = wx.Button(
            self.ServerCtrl, wx.ID_ANY, "Minimize to tray")
        self.exitSrvCtrlBtn = wx.Button(self.ServerCtrl, wx.ID_EXIT, "")
        self.LayoutPane = wx.Panel(self.Tabs, wx.ID_ANY)

        # Sets stdout to logger textctrl
        sys.stdout = self.Logger

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.onRestartWebserver,
                  self.restartWebSrvBtn)
        self.Bind(wx.EVT_BUTTON, self.onStopWebserver, self.stopWebSrvBtn)
        self.Bind(wx.EVT_BUTTON, self.onStartWebserver, self.startWebSrvBtn)
        self.Bind(wx.EVT_BUTTON, self.onRestartADB, self.restartAdbBtn)
        self.Bind(wx.EVT_BUTTON, self.onStopADB, self.stopAdbBtn)
        self.Bind(wx.EVT_BUTTON, self.onStartADB, self.startAdbBtn)
        # self.Bind(wx.EVT_BUTTON, self.onRestartADBPort,
        #           self.restartAdbTunnelBtn)
        self.Bind(wx.EVT_BUTTON, self.onMinimizeToTray, self.minimizeToTrayBtn)
        self.Bind(wx.EVT_BUTTON, self.onExitCmd, self.exitSrvCtrlBtn)

        panel = wx.Panel(self)
        self.tbIcon = GUISystemtray.GUISystemtray(self)

        self.Bind(wx.EVT_ICONIZE, self.onMinimizeToTray)
        self.Bind(wx.EVT_CLOSE, self.onClose)

    def __set_properties(self):
        self.SetTitle("Android Screen Control Server")
        self.Logger.SetBackgroundColour(wx.Colour(13, 13, 13))
        self.Logger.SetForegroundColour(wx.Colour(255, 255, 255))
        self.Logger.SetFont(wx.Font(8, wx.FONTFAMILY_SCRIPT,
                                    wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, u"Courier"))
        self.restartWebSrvBtn.SetBackgroundColour(wx.Colour(255, 198, 53))
        self.stopWebSrvBtn.SetBackgroundColour(wx.Colour(255, 127, 127))
        self.startWebSrvBtn.SetBackgroundColour(wx.Colour(91, 191, 75))
        self.restartAdbBtn.SetBackgroundColour(wx.Colour(255, 198, 53))
        self.stopAdbBtn.SetBackgroundColour(wx.Colour(255, 127, 127))
        self.startAdbBtn.SetBackgroundColour(wx.Colour(91, 191, 75))
        # self.restartAdbTunnelBtn.SetBackgroundColour(wx.Colour(255, 198, 53))
        self.reloadPluginsBtn.SetBackgroundColour(wx.Colour(255, 198, 53))

    def __do_layout(self):
        # begin wxGlade: GUIDrawer.__do_layout
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_4 = wx.GridSizer(5, 3, 0, 0)
        startPaneSplitter = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_3 = wx.GridSizer(7, 4, 0, 0)
        grid_sizer_3.Add((0, 0), 0, 0, 0)
        grid_sizer_3.Add((0, 0), 0, 0, 0)
        grid_sizer_3.Add((0, 0), 0, 0, 0)
        grid_sizer_3.Add((0, 0), 0, 0, 0)
        adbServerLbl = wx.StaticText(
            self.StartPane, wx.ID_ANY, "ADB Server:", style=wx.ALIGN_RIGHT)
        grid_sizer_3.Add(
            adbServerLbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 3)
        self.adbServerStatusLbl = wx.StaticText(
            self.StartPane, wx.ID_ANY, "Stopped", style=wx.ALIGN_LEFT)
        self.adbServerStatusLbl.SetForegroundColour(wx.Colour(207, 99, 99))
        grid_sizer_3.Add(self.adbServerStatusLbl, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 2)
        deviceLbl = wx.StaticText(
            self.StartPane, wx.ID_ANY, "Device:", style=wx.ALIGN_RIGHT)
        grid_sizer_3.Add(
            deviceLbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 3)
        self.deviceStatusLbl = wx.StaticText(
            self.StartPane, wx.ID_ANY, "<none>", style=wx.ALIGN_LEFT)
        grid_sizer_3.Add(self.deviceStatusLbl, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 3)
        adbTunnelLbl = wx.StaticText(
            self.StartPane, wx.ID_ANY, "ADB Tunnel:", style=wx.ALIGN_RIGHT)
        grid_sizer_3.Add(
            adbTunnelLbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 3)
        self.adbTunnelStatusLbl = wx.StaticText(
            self.StartPane, wx.ID_ANY, "Stopped", style=wx.ALIGN_LEFT)
        self.adbTunnelStatusLbl.SetForegroundColour(wx.Colour(207, 99, 99))
        grid_sizer_3.Add(self.adbTunnelStatusLbl, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 2)
        pluginsLbl = wx.StaticText(
            self.StartPane, wx.ID_ANY, "Plugins:", style=wx.ALIGN_RIGHT)
        grid_sizer_3.Add(
            pluginsLbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 3)
        pluginsStatusLbl = wx.StaticText(
            self.StartPane, wx.ID_ANY, "Not loaded", style=wx.ALIGN_LEFT)
        pluginsStatusLbl.SetForegroundColour(wx.Colour(207, 99, 99))
        grid_sizer_3.Add(pluginsStatusLbl, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 2)
        adbPortLbl = wx.StaticText(
            self.StartPane, wx.ID_ANY, "ADB Port:", style=wx.ALIGN_RIGHT)
        grid_sizer_3.Add(
            adbPortLbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 3)
        self.adbPortStatusLbl = wx.StaticText(
            self.StartPane, wx.ID_ANY, "<none>", style=wx.ALIGN_LEFT)
        grid_sizer_3.Add(self.adbPortStatusLbl, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 2)
        grid_sizer_3.Add((0, 0), 0, 0, 0)
        grid_sizer_3.Add((0, 0), 0, 0, 0)
        webserverLbl = wx.StaticText(
            self.StartPane, wx.ID_ANY, "Webserver:", style=wx.ALIGN_RIGHT)
        grid_sizer_3.Add(
            webserverLbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 3)
        self.webserverStatusLbl = wx.StaticText(
            self.StartPane, wx.ID_ANY, "Stopped", style=wx.ALIGN_LEFT)
        self.webserverStatusLbl.SetForegroundColour(wx.Colour(207, 99, 99))
        grid_sizer_3.Add(self.webserverStatusLbl, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 2)
        grid_sizer_3.Add((0, 0), 0, 0, 0)
        grid_sizer_3.Add((0, 0), 0, 0, 0)
        webserverHostLbl = wx.StaticText(
            self.StartPane, wx.ID_ANY, "Webserver Host:", style=wx.ALIGN_RIGHT)
        grid_sizer_3.Add(webserverHostLbl, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 3)
        self.webserverHostStatusLbl = wx.StaticText(
            self.StartPane, wx.ID_ANY, "<none>", style=wx.ALIGN_LEFT)
        grid_sizer_3.Add(self.webserverHostStatusLbl, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 3)
        grid_sizer_3.Add((0, 0), 0, 0, 0)
        grid_sizer_3.Add((0, 0), 0, 0, 0)
        webserverPortLbl = wx.StaticText(
            self.StartPane, wx.ID_ANY, "Webserver Port:", style=wx.ALIGN_RIGHT)
        grid_sizer_3.Add(webserverPortLbl, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 3)
        self.webserverPortStatusLbl = wx.StaticText(
            self.StartPane, wx.ID_ANY, "<none>", style=wx.ALIGN_LEFT)
        grid_sizer_3.Add(self.webserverPortStatusLbl, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.EXPAND, 3)
        grid_sizer_3.Add((0, 0), 0, 0, 0)
        grid_sizer_3.Add((0, 0), 0, 0, 0)
        startPaneSplitter.Add(grid_sizer_3, 1, wx.EXPAND, 0)
        LoggerLbl = wx.StaticText(
            self.StartPane, wx.ID_ANY, "Logger:", style=wx.ALIGN_LEFT)
        startPaneSplitter.Add(LoggerLbl, 0, wx.EXPAND | wx.FIXED_MINSIZE, 0)
        startPaneSplitter.Add(self.Logger, 1, wx.EXPAND, 0)
        self.StartPane.SetSizer(startPaneSplitter)
        grid_sizer_4.Add(self.restartWebSrvBtn, 0, wx.ALL | wx.EXPAND, 8)
        grid_sizer_4.Add(self.stopWebSrvBtn, 0, wx.ALL | wx.EXPAND, 8)
        grid_sizer_4.Add(self.startWebSrvBtn, 0, wx.ALL | wx.EXPAND, 8)
        grid_sizer_4.Add(self.restartAdbBtn, 0, wx.ALL | wx.EXPAND, 8)
        grid_sizer_4.Add(self.stopAdbBtn, 0, wx.ALL | wx.EXPAND, 8)
        grid_sizer_4.Add(self.startAdbBtn, 0, wx.ALL | wx.EXPAND, 8)

        # grid_sizer_4.Add(self.restartAdbTunnelBtn, 0, wx.ALL | wx.EXPAND, 8)
        grid_sizer_4.Add(wx.StaticText(self.ServerCtrl, wx.ID_ANY,
                                       " ", style=wx.Left), 0, wx.ALL | wx.EXPAND, 8)

        grid_sizer_4.Add((0, 0), 0, 0, 0)
        grid_sizer_4.Add((0, 0), 0, 0, 0)
        grid_sizer_4.Add(self.reloadPluginsBtn, 0, wx.ALL | wx.EXPAND, 8)
        grid_sizer_4.Add((0, 0), 0, 0, 0)
        grid_sizer_4.Add((0, 0), 0, 0, 0)
        grid_sizer_4.Add((0, 0), 0, 0, 0)
        grid_sizer_4.Add(self.minimizeToTrayBtn, 0, wx.ALL | wx.EXPAND, 8)
        grid_sizer_4.Add(self.exitSrvCtrlBtn, 0, wx.ALL | wx.EXPAND, 8)
        self.ServerCtrl.SetSizer(grid_sizer_4)
        self.Tabs.AddPage(self.StartPane, "Start")
        self.Tabs.AddPage(self.ServerCtrl, "Server Control")
        self.Tabs.AddPage(self.LayoutPane, "Layout")
        mainSizer.Add(self.Tabs, 1, wx.EXPAND, 0)
        self.SetSizer(mainSizer)
        self.Layout()
        # end wxGlade

    def UpdateGUI(self):
        self.SetText(self.deviceStatusLbl, 'ConnectedDeviceName', False)
        self.SetText(self.webserverHostStatusLbl, 'WebserverHost', True)
        self.SetText(self.webserverPortStatusLbl, 'WebserverPort', True)
        self._SetStatus(self.adbTunnelStatusLbl, 'ADB_Tunnel')
        self._SetStatus(self.adbServerStatusLbl, 'ADB_Status')
        self._SetStatus(self.webserverStatusLbl, 'Webserver_Status')

        self.adbPortStatusLbl.SetLabel(
            str(self.connectorRef.config['SETTINGS']['ADBTunnelHostPort']) + " : " + str(self.connectorRef.config['SETTINGS']['ADBTunnelClientPort']))

    def SetText(self, lbl, dictEntry, config):
        if(config):
            lbl.SetLabel(str(self.connectorRef.config['SETTINGS'][dictEntry]))
        else:
            lbl.SetLabel(str(self.connectorRef.guiDict[dictEntry]))

    def _SetStatus(self, lbl, dictEntry):
        ret = self._GetRunning(dictEntry)
        lbl.SetLabel(ret)
        lbl.SetForegroundColour(self._GetStatusColour(ret))

    def _GetRunning(self, guiDictEntry) -> str:
        ret = "Running" if str(
            self.connectorRef.guiDict[str(guiDictEntry)]).lower() == "true" else "Stopped"
        return ret

    def _GetStatusColour(self, ret) -> wx.Colour:
        if(ret == "Stopped"):
            return wx.Colour(207, 99, 99)
        elif(ret == "Running"):
            return wx.Colour(93, 207, 38)
        else:
            return wx.Colour(0, 0, 0)

    def onRestartWebserver(self, event):  # wxGlade: GUIDrawer.<event_handler>
        self.connectorRef.RestartWebserverThread()

    def onRestartADB(self, event):  # wxGlade: GUIDrawer.<event_handler>
        self.connectorRef.RestartADB()

    def onRestartADBPort(self, event):  # wxGlade: GUIDrawer.<event_handler>
        print("Event handler 'onRestartADBPort' not implemented!")
        event.Skip()

    def onStopADB(self, event):  # wxGlade: GUIDrawer.<event_handler>
        self.connectorRef.StopADB()

    def onExitCmd(self, event):  # wxGlade: GUIDrawer.<event_handler>
        self.Close(True)

    def onStopWebserver(self, event):  # wxGlade: GUIDrawer.<event_handler>
        self.connectorRef.onStopWebserver()

    def onStartWebserver(self, event):  # wxGlade: GUIDrawer.<event_handler>
        self.connectorRef.StartWebThread()

    def onStartADB(self, event):  # wxGlade: GUIDrawer.<event_handler>
        self.connectorRef.StartADBThread()

    #  Destroy the taskbar icon and the frame

    def onClose(self, evt):
        self.tbIcon.RemoveIcon()
        self.tbIcon.Destroy()
        self.Destroy()

    # When minimizing, hide the frame so it "minimizes to tray"
    def onMinimizeToTray(self, evt):
        self.Hide()
