import wx.lib.agw.customtreectrl as customtreectrl
from models import Notebook
import wx
from .notebook_dialog import NotebookDialog


class NoteTree(customtreectrl.CustomTreeCtrl):
    def __init__(self, parent):
        super().__init__(parent, agwStyle=customtreectrl.TR_HAS_BUTTONS | customtreectrl
                         .TR_FULL_ROW_HIGHLIGHT | customtreectrl.TR_ELLIPSIZE_LONG_ITEMS | customtreectrl
                         .TR_TOOLTIP_ON_LONG_ITEMS)

        self.root = self.AddRoot("所有笔记", data=Notebook())
        self._load_notebooks(self.root, None)
        self._init_ui()
        self._init_popup_menu()
        self._init_event()

    def _load_notebooks(self, parent_node, parent_id):
        child_notebooks = Notebook.select().where(Notebook.parent_id == parent_id)
        for notebook in child_notebooks:
            item = self.AppendItem(parent_node, notebook.name, data=notebook)
            self._load_notebooks(item, notebook.id)
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

    def _init_popup_menu(self):
        self.menu = wx.Menu()
        self.menu_id_create_notebook = wx.NewIdRef()
        self.menu_id_edit_notebook = wx.NewIdRef()
        self.menu_id_delete_notebook = wx.NewIdRef()

        self.menu.Append(self.menu_id_create_notebook, '创建笔记本')
        self.menu.Append(self.menu_id_edit_notebook, '编辑笔记本')
        self.menu.Append(self.menu_id_delete_notebook, '删除笔记本')

    def _init_event(self):
        self.Bind(wx.EVT_CONTEXT_MENU, self._show_popup_menu)
        self.Bind(wx.EVT_MENU, self._create_notebook, id=self.menu_id_create_notebook)
        self.Bind(wx.EVT_MENU, self._edit_notebook, id=self.menu_id_edit_notebook)
        self.Bind(wx.EVT_MENU, self._delete_notebook, id=self.menu_id_delete_notebook)

    def _show_popup_menu(self, _):
        self.PopupMenu(self.menu)

    def _create_notebook(self, _):
        with NotebookDialog(self) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                notebook = Notebook.create(
                    name=dialog.get_name(),
                    description=dialog.get_description(),
                    parent_id=self.GetSelection().GetData().id)
                item = self.AppendItem(self.GetSelection(), notebook.name, data=notebook)
                self.DoSelectItem(item)

    def _edit_notebook(self, _):
        notebook = self.GetSelection().GetData()
        with NotebookDialog(self, notebook) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                notebook.name = dialog.get_name()
                notebook.description = dialog.get_description()
                notebook.save()

                self.SetItemText(self.GetSelection(), notebook.name)

    def _delete_notebook(self, _):
        dialog = wx.MessageDialog(self, '此笔记本中的任何笔记都将被删除，这个操作不能恢复。', '确定要删除吗？', style=wx.OK | wx.CANCEL | wx.CANCEL_DEFAULT)
        dialog.SetOKCancelLabels('确定', '取消')

        if dialog.ShowModal() == wx.ID_OK:
            self.GetSelection().GetData().delete_instance()
            self.Delete(self.GetSelection())

    @property
    def notebook_id(self):
        return self.GetSelection().GetData().id
