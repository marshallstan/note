import wx
from .header_panel import HeaderPanel
from .note_list_panel import NoteListPanel
from pubsub import pub


class ListPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.BORDER_NONE)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.header_panel = HeaderPanel(self)
        main_sizer.Add(self.header_panel, flag=wx.EXPAND)

        self.note_list_panel = NoteListPanel(self)
        main_sizer.Add(self.note_list_panel, flag=wx.EXPAND, proportion=1)

        self.SetSizer(main_sizer)
        # self.add([1])
        pub.subscribe(self._on_note_created, 'note.created')

    def add(self, notes):
        self.note_list_panel.clear()
        self.note_list_panel.add(notes)

    def _on_note_created(self, note):
        self.add([note])
