#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Nganj
#
# Created:     12/12/2015
# Copyright:   (c) Nganj 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import wx
import os
import sys
class secondary(wx.Frame):
    def __init__(self, parent, id, table):
        self.table = table
        wx.Frame.__init__(self, parent, id, "Displaying "+self.table, size=(1000,450))
        path = os.path.abspath("./Imagesm/meter.png")
        icon = wx.Icon(path, wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)

        self.tbl = None
        parentPanel = wx.Panel(self, -1)
        self.sectoppnl = wx.Panel(parentPanel, -1)
        self.secbttmpnl = wx.Panel(parentPanel, -1)

        listsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.seclist = wx.ListCtrl(self.secbttmpnl, -1, style=wx.LC_REPORT)
        listsizer.Add(self.seclist, 1, wx.EXPAND | wx.ALL, 5)
        self.secbttmpnl.SetSizer(listsizer)

        editButton = wx.Button(self.sectoppnl, -1, " Insert / Edit ", (50, 20))
        cancelButton = wx.Button(self.sectoppnl, -1, " Cancel ", (50, 20))
        ahsizer = wx.BoxSizer(wx.HORIZONTAL)
        ahsizer.Add(editButton, 0, wx.ALL, 5)
        ahsizer.Add(cancelButton, 0, wx.ALL, 5)
        self.sectoppnl.SetSizer(ahsizer)

        self.Bind(wx.EVT_BUTTON, self.OnCancel, id = cancelButton.GetId())
        if self.table == 'accounts':
            self.tbl = accounts(self.seclist)
            self.Bind(wx.EVT_BUTTON, self.tbl.editAccounts, id = editButton.GetId())
        elif self.table == 'Location':
            self.tbl = Location(self.seclist)
            self.Bind(wx.EVT_BUTTON, self.tbl.editLocation, id = editButton.GetId())
        else:
            print 'invalid table'


        asizer = wx.BoxSizer(wx.VERTICAL)
        asizer.Add(self.sectoppnl, 0, wx.EXPAND)
        asizer.Add(self.secbttmpnl, 1, wx.EXPAND|wx.ALL, 5)
        parentPanel.SetSizer(asizer)
        self.Show()
    def OnCancel(self, event):
##        if self.table == 'accounts':
##            accounts.adlg.Destroy()
##        else:
##            Location.ldlg.Destroy()
        self.Destroy()

class Location:
    def __init__(self, llist):
        locations = [('Muchatha','The whole of muchatha area'),('Banana','The whole of banana area'),('Gachie','The whole of gachie area')]
        self.llist = llist
        self.llist.InsertColumn(0, 'Location', width = 90)
        self.llist.InsertColumn(1, 'Description', width = 120)
        for i in locations:
            index = self.llist.InsertStringItem(sys.maxint, i[0])
            self.llist.SetStringItem(index, 1, i[1])
        self.ldlg = None


if __name__ == '__main__':
    app = wx.App()
    app.MainLoop()