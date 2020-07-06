import wx
import os
from .webview import Webview
from .text_editor_toolbar import TextEditorToolbar
from pubsub import pub


class TextEditor(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.BORDER_NONE)
        self._init_ui()
        self.webview.set_js_bindings([('pyOnFormatChanged', self._on_format_changed)])
        self.content_format = {
            'bold': False,
            'font': False,
            'size': False,
            'color': False,
            'background': False,
            'code-block': False
        }
        self.note = None
        pub.subscribe(self.load_note, 'note.created')
        self.webview.set_js_bindings(
            [('pyOnFormatChanged', self._on_format_changed),
             ('pyOnContentChanged', self._on_content_changed)],
        )

    def _init_ui(self):
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self._init_title()
        self._init_toolbar()
        self._init_webview()
        self.SetSizer(self.main_sizer)
        self.SetBackgroundColour('white')

    def _init_webview(self):
        root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        editor_url = f"file://{os.path.join(root_path, 'assets', 'text_editor', 'index.html')}"

        self.webview = Webview(self)
        self.webview.load_url(editor_url)
        self.main_sizer.Add(self.webview, flag=wx.EXPAND, proportion=1)

    def _init_title(self):
        self.main_sizer.AddSpacer(20)
        self.tc_title = wx.TextCtrl(self)
        self.main_sizer.Add(self.tc_title, flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=15)
        self.main_sizer.AddSpacer(20)
        self.tc_title.Bind(wx.EVT_TEXT, self._on_title_changed)

    def _on_title_changed(self, _):
        if self.note:
            self.note.title = self.tc_title.Value.strip()
            self.note.save()
            pub.sendMessage('note.updated', note=self.note)

    def _init_toolbar(self):
        self.toolbar = TextEditorToolbar(self)
        self.main_sizer.Add(self.toolbar, flag=wx.EXPAND|wx.LEFT, border=15)

        line = wx.StaticLine(self, size=(-1, 1))
        line.SetBackgroundColour("#e5e5e5")
        self.main_sizer.Add(line, flag=wx.EXPAND|wx.TOP, border=25)

    def format_content(self, format_command, format_arg):
        self.webview.SetFocus()
        self.webview.run_js('quill.format', format_command, format_arg, 'user')
        self.content_format[format_command] = format_arg

    def _on_format_changed(self, content_format):
        changed_format = {}
        for key, val in self.content_format.items():
            format_val = content_format.pop(key, False)
            if format_val != val:
                self.content_format[key] = format_val
                changed_format[key] = format_val
        self.toolbar.display_format(changed_format)

    def load_note(self, note):
        self.note = note
        self.tc_title.ChangeValue(self.note.title)
        self.webview.run_js('quill.loadContent', self.note.content)

    def _on_content_changed(self, content):
        if self.note:
            self.note.set_content(content)
            pub.sendMessage('note.updated', note=self.note)
