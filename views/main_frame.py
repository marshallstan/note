import wx
import wx.aui
from .nav_panel import NavPanel
from .list_panel import ListPanel
from .text_editor import TextEditor


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='UltraNote', size=(800, 600))
        self.aui_manager = wx.aui.AuiManager(self, wx.aui.AUI_MGR_TRANSPARENT_HINT)

        self.nav_panel = NavPanel(self)
        self.list_panel = ListPanel(self)
        self.detail_panel = TextEditor(self)

        self.aui_manager.AddPane(self.nav_panel, self._get_default_pane_info().Left()
                                 .Row(0).BestSize(300, -1))
        self.aui_manager.AddPane(self.list_panel, self._get_default_pane_info().Left()
                                 .Row(1).BestSize(250, -1).MinSize(150, -1))
        self.aui_manager.AddPane(self.detail_panel, self._get_default_pane_info()
                                 .CenterPane().Position(0).BestSize(400, -1))

        self.aui_manager.GetArtProvider().SetMetric(wx.aui.AUI_DOCKART_SASH_SIZE, 1)
        self.aui_manager.Update()

        self.Maximize(True)
        self._register_listeners()

    @staticmethod
    def _get_default_pane_info():
        return wx.aui.AuiPaneInfo().CaptionVisible(False).PaneBorder(False)\
            .CloseButton(False).PinButton(False).Gripper(False)

    def on_frame_closing(self, e):
        self.aui_manager.UnInit()
        del self.aui_manager
        self.Destroy()

    def _register_listeners(self):
        self.Bind(wx.EVT_CLOSE, self.on_frame_closing)
