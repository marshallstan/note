import wx
from .generic_bitmap_button import GenericBitmapButton
from models import Note
from functools import partial
from pubsub import pub


class HeaderPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.BORDER_NONE)
        self._init_ui()
        self.note_count = 0
        self._sort_menu_ids = wx.NewIdRef(6)
        self._checked_menu_id = self._sort_menu_ids[0]
        self.sort_option = Note.updated_at.desc()
        self._rename_notebook_menu_id = wx.NewIdRef()
        self._delete_notebook_menu_id = wx.NewIdRef()
        self._init_event()

    def _init_ui(self):
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.st_notebook_name = wx.StaticText(self, label='笔记本名称')
        self.main_sizer.Add(self.st_notebook_name, flag=wx.ALL, border=10)

        self._build_note_actions()
        self._build_search_bar()
        self.main_sizer.AddSpacer(10)
        self.SetSizer(self.main_sizer)

        self.SetBackgroundColour("#ebebeb")

    def _init_event(self):
        self.btn_display_order_options.Bind(wx.EVT_BUTTON, self._show_sort_menu)
        self.Bind(wx.EVT_MENU, partial(self._on_note_sorting, sort_param=Note.updated_at.desc()), id=self._sort_menu_ids[0])
        self.Bind(wx.EVT_MENU, partial(self._on_note_sorting, sort_param=Note.updated_at.asc()), id=self._sort_menu_ids[1])
        self.Bind(wx.EVT_MENU, partial(self._on_note_sorting, sort_param=Note.created_at.desc()), id=self._sort_menu_ids[2])
        self.Bind(wx.EVT_MENU, partial(self._on_note_sorting, sort_param=Note.created_at.asc()), id=self._sort_menu_ids[3])
        self.Bind(wx.EVT_MENU, partial(self._on_note_sorting, sort_param=Note.title.desc()), id=self._sort_menu_ids[4])
        self.Bind(wx.EVT_MENU, partial(self._on_note_sorting, sort_param=Note.title.asc()), id=self._sort_menu_ids[5])
        self.Bind(wx.EVT_MENU, partial(self._on_note_sorting, sort_param=Note.title.asc()), id=self._sort_menu_ids[5])
        self.btn_display_notebook_options.Bind(wx.EVT_BUTTON, self._show_action_menu)
        self.Bind(wx.EVT_MENU, lambda _: pub.sendMessage('notebook.editing'), id=self._rename_notebook_menu_id)
        self.Bind(wx.EVT_MENU, lambda _: pub.sendMessage('notebook.deleting'), id=self._delete_notebook_menu_id)

    def _show_sort_menu(self, _):
        menu = self._build_sort_menu()
        menu.Check(self._checked_menu_id, True)
        self.PopupMenu(menu)
        menu.Destroy()

    def _on_note_sorting(self, e, sort_param):
        if self._checked_menu_id != e.GetId():
            self._checked_menu_id = e.GetId()
            self.sort_option = sort_param
            pub.sendMessage('note.sorting', sort_param=sort_param)

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

    def _build_sort_menu(self):
        menu = wx.Menu()

        sub_menu1 = wx.Menu()
        sub_menu1.AppendCheckItem(self._sort_menu_ids[0], '最新到最旧')
        sub_menu1.AppendCheckItem(self._sort_menu_ids[1], '最旧到最新')
        menu.AppendSubMenu(sub_menu1, '按更新时间')

        sub_menu2 = wx.Menu()
        sub_menu2.AppendCheckItem(self._sort_menu_ids[2], '最新到最旧')
        sub_menu2.AppendCheckItem(self._sort_menu_ids[3], '最旧到最新')
        menu.AppendSubMenu(sub_menu2, '按创建时间')

        sub_menu3 = wx.Menu()
        sub_menu3.AppendCheckItem(self._sort_menu_ids[4], '逆字母排序')
        sub_menu3.AppendCheckItem(self._sort_menu_ids[5], '字母排序')
        menu.AppendSubMenu(sub_menu3, '按标题')

        return menu

    def _show_action_menu(self, _):
        menu = self._build_action_menu()
        self.PopupMenu(menu)
        menu.Destroy()
