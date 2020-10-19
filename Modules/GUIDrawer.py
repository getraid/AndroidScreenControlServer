# native
import atexit
# pip packages
import wx
import sys


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

        self.SetSize((700, 400))
        self.Tabs = wx.Notebook(self, wx.ID_ANY)
        self.StartPane = wx.Panel(self.Tabs, wx.ID_ANY)
        self.Logger = wx.TextCtrl(self.StartPane, wx.ID_ANY, "",
                                  style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP)
        self.LayoutPane = wx.Panel(self.Tabs, wx.ID_ANY)
        sys.stdout = self.Logger

        self.frame_menubar = wx.MenuBar()
        wx_menubar = wx.Menu()
        item = wx_menubar.Append(
            wx.ID_ANY, "Restart Webserver", "Restarts the included webserver")
        self.Bind(wx.EVT_MENU, self.on_menu_Restart_Webserver, id=item.GetId())
        wx_menubar.AppendSeparator()
        item = wx_menubar.Append(
            wx.ID_ANY, "Restart ADB", "Restarts ADB Server")
        self.Bind(wx.EVT_MENU, self.on_menu_Restart_ADB, id=item.GetId())
        item = wx_menubar.Append(
            wx.ID_ANY, "Reconnect ADB Port", "Creates internal reverse proxy through USB")
        self.Bind(wx.EVT_MENU, self.on_menu_Restart_ADB_Port, id=item.GetId())
        item = wx_menubar.Append(
            wx.ID_ANY, "Stop ADB", "Stops ADB Server")
        self.Bind(wx.EVT_MENU, self.on_menu_Stop_ADB, id=item.GetId())
        wx_menubar.AppendSeparator()
        item = wx_menubar.Append(
            wx.ID_ANY, "Minimize to Tray", "Minimizes window to system tray")
        self.Bind(wx.EVT_MENU, self.on_menu_Minimize_To_Tray, id=item.GetId())
        item = wx_menubar.Append(
            wx.ID_ANY, "Exit", "Stops all servers and closes the program.")
        self.Bind(wx.EVT_MENU, self.on_menu_File_Exit, id=item.GetId())
        self.frame_menubar.Append(wx_menubar, "Quick Options")
        self.SetMenuBar(self.frame_menubar)

        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        self.SetTitle("frame")
        self.Logger.SetBackgroundColour(wx.Colour(88, 88, 88))
        self.Logger.SetForegroundColour(wx.Colour(255, 255, 255))
        self.Logger.SetFont(wx.Font(10, wx.FONTFAMILY_MODERN,
                                    wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Courier"))

    def __do_layout(self):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        startPaneSplitter = wx.BoxSizer(wx.VERTICAL)
        startPaneGrid = wx.GridSizer(8, 2, 0, 0)
        startPaneGrid.Add((0, 0), 0, 0, 0)
        startPaneGrid.Add((0, 0), 0, 0, 0)
        startPaneGrid.Add((0, 0), 0, 0, 0)
        startPaneGrid.Add((0, 0), 0, 0, 0)
        startPaneGrid.Add((0, 0), 0, 0, 0)
        startPaneGrid.Add((0, 0), 0, 0, 0)
        startPaneGrid.Add((0, 0), 0, 0, 0)
        startPaneGrid.Add((0, 0), 0, 0, 0)
        startPaneGrid.Add((0, 0), 0, 0, 0)
        startPaneGrid.Add((0, 0), 0, 0, 0)
        startPaneGrid.Add((0, 0), 0, 0, 0)
        startPaneGrid.Add((0, 0), 0, 0, 0)
        startPaneGrid.Add((0, 0), 0, 0, 0)
        startPaneGrid.Add((0, 0), 0, 0, 0)
        startPaneGrid.Add((0, 0), 0, 0, 0)
        startPaneGrid.Add((0, 0), 0, 0, 0)
        startPaneSplitter.Add(startPaneGrid, 2, wx.EXPAND, 0)
        startPaneSplitter.Add(self.Logger, 1, wx.EXPAND, 0)
        self.StartPane.SetSizer(startPaneSplitter)
        self.Tabs.AddPage(self.StartPane, "Start")
        self.Tabs.AddPage(self.LayoutPane, "Layout")
        mainSizer.Add(self.Tabs, 1, wx.EXPAND, 0)
        self.SetSizer(mainSizer)
        self.Layout()

    def on_menu_Restart_Webserver(self, event):
        print("Event handler 'on_menu_Restart_Webserver' not implemented!")
        event.Skip()

    def on_menu_Restart_ADB(self, event):
        print("Event handler 'on_menu_Restart_ADB' not implemented!")
        event.Skip()

    def on_menu_Restart_ADB_Port(self, event):
        print("Event handler 'on_menu_Restart_ADB_Port' not implemented!")
        event.Skip()

    def on_menu_Stop_ADB(self, event):
        print("Event handler 'on_menu_Stop_ADB' not implemented!")
        event.Skip()

    def on_menu_Minimize_To_Tray(self, event):
        print("Event handler 'on_menu_Minimize_To_Tray' not implemented!")
        event.Skip()

    def on_menu_File_Exit(self, event):
        self.Close(True)
