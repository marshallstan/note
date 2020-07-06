import wx
from .note_preview_panel import NotePreviewPanel
import wx.lib.scrolledpanel as scrolled
import images
from pubsub import pub


class NoteListPanel(scrolled.ScrolledPanel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.VSCROLL)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self._init_empty_sizer()
        self._init_list_sizer()
        self.SetSizer(self.main_sizer)
        self.SetBackgroundColour('white')
        self.SetupScrolling(scroll_x=False)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.selected_note = None
        pub.subscribe(self._on_note_updated, 'note.updated')

    def on_size(self, evt):
        size = self.GetSize()
        vsize = self.GetVirtualSize()
        self.SetVirtualSize((size[0], vsize[1]))
        evt.Skip()

    def _init_empty_sizer(self):
        self.empty_msg_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.empty_msg_sizer, flag=wx.EXPAND, proportion=1)

        self.empty_msg_sizer.AddStretchSpacer()
        self.empty_msg_sizer.Add(wx.StaticBitmap(self, bitmap=images.empty_note.GetBitmap()), flag=wx.CENTER)
        self.empty_msg_sizer.Add(wx.StaticText(self, label='未找到笔记'), flag=wx.CENTER | wx.TOP, border=10)
        self.empty_msg_sizer.AddStretchSpacer()

    def _init_list_sizer(self):
        self.list_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.list_sizer, flag=wx.EXPAND, proportion=1)

    def add(self, notes):
        self.show_empty(False)

        preview_panels = list((NotePreviewPanel(self, note), 0, wx.EXPAND) for note in notes)
        self.list_sizer.AddMany(preview_panels)

    def clear(self):
        self.selected_note = None
        self.list_sizer.Clear(True)
        self.show_empty(True)

    def show_empty(self, show=True):
        if show and not self.main_sizer.IsShown(self.empty_msg_sizer):
            pub.sendMessage('note.empty')
            self.main_sizer.Show(self.empty_msg_sizer, True)
        if not show and self.main_sizer.IsShown(self.empty_msg_sizer):
            self.main_sizer.Show(self.empty_msg_sizer, False)
        self.SetupScrolling(scroll_x=False)

    def prepend(self, note):
        self.list_sizer.Prepend(NotePreviewPanel(self, note), flag=wx.EXPAND)
        self.show_empty(False)

    def remove(self, note):
        preview_panel = self._get_preview_panel(note)
        self.list_sizer.Detach(preview_panel)
        preview_panel.DestroyLater()
        if self.list_sizer.IsEmpty():
            self.show_empty(True)
        else:
            self.SetupScrolling(scroll_x=False)

    def replace(self, notes, preserve_select=False):
        self.list_sizer.Clear(True)
        preview_panels = list((NotePreviewPanel(self, note), 0, wx.EXPAND) for note in notes)
        self.list_sizer.AddMany(preview_panels)
        self.show_empty(False)
        if preserve_select:
            if self.selected_note:
                self._get_preview_panel(self.selected_note).focus(True)
        else:
            self.selected_note = None
            self.select(notes[0])

    def select(self, note):
        if self.selected_note:
            self._get_preview_panel(self.selected_note).focus(False)
        self._get_preview_panel(note).focus()
        self.selected_note = note
        pub.sendMessage('note.selected', note=self.selected_note)

    def _on_note_updated(self, note):
        if self.selected_note:
            self._get_preview_panel(self.selected_note).update(note)

    def _get_preview_panel(self, note):
        return self.FindWindowByName(f"preview_{note.id}", self)
