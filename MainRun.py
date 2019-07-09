import csv
import webbrowser
import pyperclip

import wx


class bucky(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, '反混淆 v1.0', size=(350, 280),
                          style=wx.CAPTION | wx.MINIMIZE_BOX | wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.STAY_ON_TOP)

        panel = wx.Panel(self)

        self.filename = ['fields.csv', 'methods.csv', 'params.csv']
        self.keyword = 'searge'
        self.target = ''

        lblList = ['fields', 'methods', 'params']
        self.rbox = wx.RadioBox(panel, label='searched from', pos=(20, 10), choices=lblList,
                                majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rbox.Enable(False)
        wx.StaticText(panel, -1, '——————————————————————————————————————————————————————————————————',
                      (0, 85)).SetForegroundColour('gray')

        wx.StaticText(panel, -1, 'target', (10, 120))
        self.seargeinput = wx.TextCtrl(panel, -1, self.target, style=wx.TE_PROCESS_ENTER, pos=(70, 120),
                                       size=(180, 20))
        self.searchbt = wx.Button(panel, -1, 'search', pos=(260, 115), size=(60, 30))

        wx.StaticText(panel, -1, 'name', pos=(10, 160))
        self.trueName = wx.TextCtrl(panel, -1, '', pos=(70, 160), size=(180, 20))
        self.trueName.SetEditable(False)

        self.openLinkbt = wx.Button(panel, -1, 'openlink', pos=(130, 200), size=(60, 30))

        self.rbox.Bind(wx.EVT_RADIOBOX, self.onRadioBox)
        self.Bind(wx.EVT_TEXT_ENTER, self.onSearch, self.seargeinput)
        self.Bind(wx.EVT_BUTTON, self.onSearch, self.searchbt)
        self.Bind(wx.EVT_BUTTON, self.openlink, self.openLinkbt)
        self.Bind(wx.EVT_CLOSE, self.closewindow)

    def onRadioBox(self, e):
        self.filename = self.rbox.GetStringSelection() + '.csv'
        if self.rbox.GetStringSelection() == 'params':
            self.keyword = 'param'
        else:
            self.keyword = 'searge'

    def onSearch(self, e):
        self.target = self.seargeinput.GetValue()

        if self.searchInFile(self.filename[0]):
            self.rbox.SetSelection(0)
        elif self.searchInFile(self.filename[1]):
            self.rbox.SetSelection(1)
        elif self.searchInFile(self.filename[2]):
            self.rbox.SetSelection(2)

    def searchInFile(self, file):
        flag = False
        with open(file, newline="\n") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data = row
                searge = data[self.keyword]
                if searge == self.target:
                    mcpName = data['name']
                    print(mcpName)
                    self.trueName.SetValue(mcpName)
                    pyperclip.copy(mcpName)
                    flag = True

        return flag

    def openlink(self, e):
        webbrowser.open('http://export.mcpbot.bspk.rs/snapshot/')

    def closewindow(self, event):
        self.Destroy()


if __name__ == '__main__':
    app = wx.App()
    frame = bucky(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
