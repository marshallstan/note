import wx
from .header_panel import HeaderPanel
from .note_list_panel import NoteListPanel


class ListPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.BORDER_NONE)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.header_panel = HeaderPanel(self)
        main_sizer.Add(self.header_panel, flag=wx.EXPAND)

        self.note_list_panel = NoteListPanel(self)
        main_sizer.Add(self.note_list_panel, flag=wx.EXPAND, proportion=1)

        self.SetSizer(main_sizer)
        self.add([1, 2, 3])

    def add(self, notes):
        self.note_list_panel.clear()
        self.note_list_panel.add(notes)
