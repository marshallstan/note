import wx
from .generic_bitmap_button import GenericBitmapButton


class HeaderPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.BORDER_NONE)
        self._init_ui()
        self.note_count = 0

    def _init_ui(self):
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.st_notebook_name = wx.StaticText(self, label='笔记本名称')
        self.main_sizer.Add(self.st_notebook_name, flag=wx.ALL, border=10)

        self._build_note_actions()
        self._build_search_bar()
        self.main_sizer.AddSpacer(10)
        self.SetSizer(self.main_sizer)

        self.SetBackgroundColour("#ebebeb")

    def _build_note_actions(self):
        note_action_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.st_note_count = wx.StaticText(self, label="10条笔记")
        note_action_sizer.Add(self.st_note_count)

        note_action_sizer.AddStretchSpacer()

        self.btn_display_order_options = GenericBitmapButton(self, 'sort')
        note_action_sizer.Add(self.btn_display_order_options)

        self.btn_display_notebook_options = GenericBitmapButton(self, 'more')
        note_action_sizer.Add(self.btn_display_notebook_options, flag=wx.LEFT, border=10)

        self.main_sizer.Add(note_action_sizer, flag=wx.ALL | wx.EXPAND, border=10)

    def _build_search_bar(self):
        self.search_bar = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.search_bar.ShowCancelButton(True)

        search_menu = wx.Menu()
        search_menu.AppendCheckItem(wx.ID_ANY, '搜索所有笔记本')
        self.search_bar.SetMenu(search_menu)
        self.search_bar.SetHint('搜索当前笔记本')

        self.main_sizer.Add(self.search_bar, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=8)

    def set_title(self, title):
        self.st_notebook_name.SetLabel(title)

    def set_count(self, count):
        self.note_count = count
        self.st_note_count.SetLabel(f'{self.note_count}条笔记')

    def change_count(self, changed_count):
        self.note_count += changed_count
        self.st_note_count.SetLabel(f'{self.note_count}条笔记')
