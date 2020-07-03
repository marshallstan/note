import wx
from wx.lib.buttons import GenButton


class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='秒表')
        self.total_seconds = 0
        self.timer = wx.Timer(self)
        self._init_ui()
        self._init_event()

    def _init_event(self):
        self.btn_run.Bind(wx.EVT_BUTTON, self._on_btn_run_clicked)
        self.btn_reset.Bind(wx.EVT_BUTTON, self._on_btn_reset_clicked)
        self.Bind(wx.EVT_TIMER, self._update_time, self.timer)

    def _on_btn_run_clicked(self, _):
        if self.timer.IsRunning():
            self.timer.Stop()
            self.btn_run.SetLabel('继续')
        else:
            self.timer.Start(1000)
            self.btn_run.SetLabel('暂停')

    def _on_btn_reset_clicked(self, _):
        self.timer.Stop()
        self.btn_run.SetLabel('开始')
        self.total_seconds = 0
        self.st_time.SetLabel('00 : 00 : 00')

    def _update_time(self, _):
        self.total_seconds += 1
        second = self.total_seconds % 60
        minute = int((self.total_seconds / 60) % 60)
        hour = int((self.total_seconds / 3600) % 24)
        self.st_time.SetLabel(f'{hour:02} : {minute:02} : {second:02}')

    def _init_ui(self):
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.AddStretchSpacer()

        self.st_time = wx.StaticText(self, label='00 : 00 : 00')
        self.st_time.SetFont(wx.Font(wx.FontInfo(120)))

        self.btn_run = GenButton(self, label='开始', size=(100,30), style=wx.BORDER_NONE)
        self.btn_reset = GenButton(self, label='复位', size=(100,30), style=wx.BORDER_NONE)

        main_sizer.Add(self.st_time, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(80)

        main_sizer.Add(self.btn_run, flag=wx.ALIGN_CENTER_HORIZONTAL)
        main_sizer.AddSpacer(30)
        main_sizer.Add(self.btn_reset, flag=wx.ALIGN_CENTER_HORIZONTAL)

        main_sizer.AddStretchSpacer()
        self.SetSizer(main_sizer)
        self.Maximize()

        self.st_time.SetForegroundColour('white')
        self.btn_run.SetBackgroundColour('#00CC99')
        self.btn_run.SetForegroundColour('white')
        self.btn_reset.SetBackgroundColour('#FF6666')
        self.btn_reset.SetForegroundColour('white')
        self.SetBackgroundColour('#444444')


app = wx.App()
MainFrame().Show()
app.MainLoop()