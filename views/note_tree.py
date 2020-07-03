import wx.lib.agw.customtreectrl as customtreectrl
from models import Notebook


class NoteTree(customtreectrl.CustomTreeCtrl):
    def __init__(self, parent):
        super().__init__(parent, agwStyle=customtreectrl.TR_HAS_BUTTONS | customtreectrl
                         .TR_FULL_ROW_HIGHLIGHT | customtreectrl.TR_ELLIPSIZE_LONG_ITEMS | customtreectrl
                         .TR_TOOLTIP_ON_LONG_ITEMS)

        self.root = self.AddRoot("所有笔记")
        self._load_note_books()
        self._init_ui()

    def _load_note_books(self):
        for notebook in Notebook.select():
            self.AppendItem(self.root, notebook.name)
        self.ExpandAll()

    def _init_ui(self):
        panel_font = self.GetFont()
        panel_font.SetPointSize(panel_font.GetPointSize() + 1)
        self.SetFont(panel_font)

        self.EnableSelectionGradient(False)
        self.EnableSelectionGradient(False)

        self.SetForegroundColour('#ececec')
        self.SetBackgroundColour('#2a2a2a')
        self.SetHilightFocusColour('#646464')
        self.SetHilightNonFocusColour('#646464')

        self.SetSpacing(20)
        self.SetIndent(10)
