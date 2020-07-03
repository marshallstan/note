import wx


class NotePreviewPanel(wx.Panel):
    def __init__(self, parent, note):
        super().__init__(parent, size=(-1, 110), style=wx.BORDER_NONE)
        self._init_ui()

    def _init_ui(self):
        v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.st_note_title = wx.StaticText(self, style=wx.ST_ELLIPSIZE_END)
        self.st_note_preview = wx.StaticText(self, style=wx.ST_ELLIPSIZE_END)
        self.st_note_date = wx.StaticText(self, label='2020-03-04')

        self.st_note_title.SetFont(wx.Font(wx.FontInfo(14).Bold()))
        self.st_note_preview.SetFont(wx.Font(wx.FontInfo(14).Light()))
        self.st_note_preview.SetForegroundColour('#4e4e4e')
        self.st_note_date.SetForegroundColour('#4e4e4e')

        v_sizer.Add(self.st_note_title, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)
        v_sizer.AddSpacer(15)
        v_sizer.Add(self.st_note_preview, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        v_sizer.AddStretchSpacer(1)
        v_sizer.Add(self.st_note_date, flag=wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        self.st_note_title.SetLabel('标题内容特别长的时候，机会显示省略号')
        self.st_note_preview.SetLabel('笔记预览内容特别长的时候，也会显示省略号')

        line = wx.StaticLine(self, size=(-1, 1))
        line.SetBackgroundColour("#cbcbcb")
        v_sizer.Add(line, flag=wx.EXPAND)

        self.SetSizer(v_sizer)
