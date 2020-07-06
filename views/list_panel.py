import wx
from .header_panel import HeaderPanel
from .note_list_panel import NoteListPanel
from pubsub import pub
from models.note import Note


class ListPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.BORDER_NONE)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.header_panel = HeaderPanel(self)
        main_sizer.Add(self.header_panel, flag=wx.EXPAND)

        self.note_list_panel = NoteListPanel(self)
        main_sizer.Add(self.note_list_panel, flag=wx.EXPAND, proportion=1)

        self.SetSizer(main_sizer)

        self._note_ids = []
        pub.subscribe(self._on_notebook_selected, 'notebook.selected')
        pub.subscribe(self._on_root_selected, 'root.selected')
        pub.subscribe(self._on_note_created, 'note.created')
        pub.subscribe(self._on_note_deleting, 'note.deleting')

    def add(self, notes):
        self.note_list_panel.clear()
        self.note_list_panel.add(notes)

    def _on_note_created(self, note):
        self.header_panel.change_count(1)
        self.note_list_panel.prepend(note)
        self.note_list_panel.select(note)
        self._note_ids.insert(0, note.id)

    def _on_notebook_selected(self, notebook):
        notes = list(notebook.notes.order_by(Note.updated_at.desc()))
        self.header_panel.set_title(notebook.name)
        self.header_panel.set_count(len(notes))
        self._load(notes)

    def _on_root_selected(self):
        notes = list(Note.select().order_by(Note.updated_at.desc()))
        self.header_panel.set_title('所有笔记')
        self.header_panel.set_count(len(notes))
        self._load(notes)

    def _load(self, notes):
        if len(notes):
            self.note_list_panel.replace(notes)
            self.note_list_panel.select(notes[0])
        else:
            self.note_list_panel.clear()
        self._note_ids = list(map(lambda note: note.id, notes))

    def _on_note_deleting(self, note):
        note.delete_instance()
        self.note_list_panel.remove(note)
        if len(self._note_ids) > 1:
            note_id_index = self._note_ids.index(note.id)
            next_index = note_id_index + 1
            if next_index > len(self._note_ids) - 1:
                next_index = note_id_index - 1
            self.note_list_panel.select(Note.get_by_id(self._note_ids[next_index]))
        self._note_ids.remove(note.id)
        self.header_panel.change_count(-1)
