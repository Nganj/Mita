#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Nganj
#
# Created:     13/10/2015
# Copyright:   (c) Nganj 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import wx
import MySQLdb
import os
import sys
import newclient
mainname ='Main'
packages = [('jessica alba', 'pomona', '1981'), ('sigourney weaver', 'new york', '1949'),
('angelina jolie', 'los angeles', '1975'), ('natalie portman', 'jerusalem', '1981'),
('rachel weiss', 'london', '1971'), ('scarlett johansson', 'new york', '1984' )]
pack = [('jessic alba', 'pomna', '1981'), ('sigourney weaver', 'new york', '1949'),
('angelina jolie', 'los angeles', '1975'), ('natalie portman', 'jerusalem', '1981'),
('rachel weiss', 'london', '1971'), ('scartt johansson', 'new york', '1984' )]
class Main(wx.Frame):
    def __init__(self, parent, id, table, maindbpool):
        wx.Frame.__init__(self, parent, id, table, size=(1100, 450), style = wx.DEFAULT_FRAME_STYLE)
        path = os.path.abspath("./Imagesm/meter.png")
        icon = wx.Icon(path, wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)
        self.maindbpool = maindbpool
        self.mode = 0
        parentPanel = wx.Panel(self, -1, size= (-1,-1))
        vsizer = wx.BoxSizer(wx.VERTICAL)
        topPanel  = wx.Panel(parentPanel, -1, size=(-1, 60))
        topPanel.SetBackgroundColour('green')
        newButton = wx.Button(topPanel, -1, "New", (50, 20))
        self.Bind(wx.EVT_BUTTON, self.newClient, id=newButton.GetId())
        editButton = wx.Button(topPanel, -1, "Edit", (50, 20))
        self.Bind(wx.EVT_BUTTON, self.editTables, id=editButton.GetId())
        closeButton = wx.Button(topPanel, -1, "Close", (50, 20))
        self.Bind(wx.EVT_BUTTON, self.OnClose, id=closeButton.GetId())
        self.newsearch = wx.SearchCtrl(topPanel, size=(120, -1), style=wx.TE_PROCESS_ENTER)
        exportButton = wx.Button(topPanel, -1, "Export", (50, 20))
        htopsizer = wx.BoxSizer(wx.HORIZONTAL)
        htopsizer.Add(newButton, 0, wx.EXPAND | wx.ALL, 5)
        htopsizer.Add(editButton, 0, wx.EXPAND | wx.ALL, 5)
        htopsizer.Add(closeButton, 0, wx.EXPAND | wx.ALL, 5)
        htopsizer.Add(self.newsearch, 0, wx.EXPAND | wx.ALL, 5)
        htopsizer.Add(exportButton, 0, wx.EXPAND | wx.ALL, 5)
        topPanel.SetSizer(htopsizer)
        self.bottomPanel = wx.Panel(parentPanel, -1, size = (-1,-1))
        self.wlist = wx.ListCtrl(self.bottomPanel, -1, style=wx.LC_REPORT)
        tabler = ['Employees','Location','Customers']
        self.tblname = table
        if self.tblname == 'Employees':
            self.tbl = Employees(self.wlist, self.maindbpool, self.bottomPanel)
        elif self.tblname == 'Customers':
            self.tbl = Customers(self.wlist, self.maindbpool, self.bottomPanel)
        elif self.tblname == 'Chat':
            print 'Chatting'
        else:
            print 'invalid table'
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox.Add(self.wlist, 1, wx.EXPAND | wx.ALL, 5)
        self.bottomPanel.SetSizer(self.hbox)
        vsizer.Add(topPanel, 0, wx.EXPAND)
        vsizer.Add(self.bottomPanel, 1, wx.EXPAND | wx.ALL, 5)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.status = None
        parentPanel.SetSizer(vsizer)
        self.Show()
    def newClient(self, event):
        self.mode = 0
        newclient.NewClient(None, -1, self.tblname, id, self.status, self.maindbpool)
    def editTables(self, event):
        self.mode = 1
        newclient.NewClient(None, -1, self.tblname, id, self.status, self.maindbpool)
    def OnClose(self, event):
        self.Destroy()
    def OnCloseWindow(self, event):
        self.Destroy()
class Employees:
    ##message = "hello"
    def __init__(self, elist, maindbpool, ePanel):
        self.ePanel = ePanel
        self.elist = elist
        self.empid = None
        self.emaindbpool = maindbpool
        self.empdeferred = self.getEmployees()
        self.empdeferred.addCallback(self.listemps)


        self.elist.InsertColumn(0, 'Employee Code', width=100)
        self.elist.InsertColumn(1, 'First Name', width=140)
        self.elist.InsertColumn(2, 'Second name', width=130)
        self.elist.InsertColumn(3, 'Last Name', wx.LIST_FORMAT_RIGHT, 90)
        self.elist.InsertColumn(4, 'Email', width=130)
        self.elist.InsertColumn(5, 'Phone Number', wx.LIST_FORMAT_RIGHT, 120)
        self.elist.InsertColumn(6, 'Physical Address', width=130)
        self.elist.InsertColumn(7, 'Username', wx.LIST_FORMAT_RIGHT, 90)
        self.elist.InsertColumn(8, 'Location', width=130)

        self.popupmenu = wx.Menu()
        self.ePanel.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.elist)
        for text in "Edit Delete".split():
                item = self.popupmenu.Append(-1, text)
                self.elist.Bind(wx.EVT_MENU, self.OnPopupItemSelected, item)
        self.ePanel.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightClickItem, self.elist)


    def OnRightClickItem(self, event):
        pos = event.GetPosition()
##        width, height = pos
##        dimen = (width, height*2)
        pos = self.elist.ScreenToClient(pos)
        self.elist.PopupMenu(self.popupmenu, pos)
    def OnDoubleClick(self, event):
        #edit on double click, not implemented
        newclient.NewClient(self.ePanel, -1, 'Employees', self.empid, 'Edit', self.emaindbpool)
    def OnPopupItemSelected(self, event):
        item = self.popupmenu.FindItemById(event.GetId())
        text = item.GetText()
        if text == 'Edit':
            newclient.NewClient(self.ePanel, -1, 'Employees', self.empid, text, self.emaindbpool)
        if text == 'Delete':
            newclient.NewClient(self.ePanel, -1, 'Employees', self.empid, text, self.emaindbpool)
##        wx.MessageBox("You selected item '%s'" % text)
    def OnItemSelected(self, event):
        item = event.GetItem()
        self.empid =  int(item.GetText())

    def listemps(self, emps):
##        self.emp = emps
##        return self.emp
        '''format employee ids'''
        def formatdate(value):
            if value < 10:
                value = '000'+ str(value)
            elif value < 100:
                value = '00'+str(value)
            else:
                value = '0'+str(value)
            return value
        for i in emps:
            index = self.elist.InsertStringItem(sys.maxint,formatdate(i[0]))
            self.elist.SetStringItem(index, 1, str(i[1]))
            self.elist.SetStringItem(index, 2, str(i[2]))
            self.elist.SetStringItem(index, 3, str(i[3]))
            self.elist.SetStringItem(index, 4, str(i[4]))
            self.elist.SetStringItem(index, 5, str(i[5]))
            self.elist.SetStringItem(index, 6, str(i[6]))
            self.elist.SetStringItem(index, 7, str(i[7]))
            self.elist.SetStringItem(index, 8, str(i[8]))
    def getEmployees(self):
        return self.emaindbpool.runQuery('select  a.emp_id, a.f_name, a.s_name, a.l_name, a.email, a.phone_no, a.physical_address, c.username, b.location from employees a left join location b on b.location_id = a.location_location_id left join credentials c on a.credentials_user_id = c.user_id ORDER BY a.emp_id')

class Customers:
    def __init__(self, clist, cdbpool, cPanel):
        self.clist = clist
        self.cdbpool = cdbpool
        self.cPanel = cPanel

        #clients might be in projects
        self.clist = clist
        self.clist.InsertColumn(0, 'Customer Index', width=120)
        self.clist.InsertColumn(1, 'First Name', width=100)
        self.clist.InsertColumn(2, 'Second Name', wx.LIST_FORMAT_RIGHT, 120)
        self.clist.InsertColumn(3, 'Last Name', wx.LIST_FORMAT_RIGHT, 120)
        self.clist.InsertColumn(4, 'Phone', wx.LIST_FORMAT_RIGHT, 100)
        self.clist.InsertColumn(5, 'Email', wx.LIST_FORMAT_RIGHT, 100)
        self.clist.InsertColumn(6, 'Meter Name', wx.LIST_FORMAT_RIGHT, 120)
        self.clist.InsertColumn(7, 'Line Name', wx.LIST_FORMAT_RIGHT, 80)
        self.clist.InsertColumn(8, 'Account Name', wx.LIST_FORMAT_RIGHT, 100)
        qt = self.query_db(""" select a.client_id, a.f_name, a.s_name, a.l_name, a.phone, a.email, b.meter_no, c.line_name, d.account_no from clients a left join meter b on a.meter_meter_id = b.meter_id left join sublocation c on a.subloc_fgn = c.sub_id left join accounts d on a.accounts_off = d.acc_id""")
        qt.addCallback(self.populate_cus_list)
        self.popupmenu = wx.Menu()
        self.cPanel.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.clist)
        for text in "Edit Delete".split():
                item = self.popupmenu.Append(-1, text)
                self.clist.Bind(wx.EVT_MENU, self.OnPopupItemSelected, item)
        self.cPanel.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightClickItem, self.clist)
    def OnRightClickItem(self, event):
        pos = event.GetPosition()
##        width, height = pos
##        dimen = (width, height*2)
        pos = self.clist.ScreenToClient(pos)
        self.clist.PopupMenu(self.popupmenu, pos)
    def OnDoubleClick(self, event):
        #edit on double click, not implemented
        newclient.NewClient(self.ePanel, -1, 'Customers', self.cid, 'Edit', self.cdbpool)
    def OnPopupItemSelected(self, event):
        item = self.popupmenu.FindItemById(event.GetId())
        text = item.GetText()
        if text == 'Edit':
            newclient.NewClient(self.cPanel, -1, 'Customers', self.cid, text, self.cdbpool)
        if text == 'Delete':
            newclient.NewClient(self.cPanel, -1, 'Customers', self.cid, text, self.cdbpool)
##        wx.MessageBox("You selected item '%s'" % text)
    def OnItemSelected(self, event):
        item = event.GetItem()
        self.cid =  int(item.GetText())
    def query_db(self, query):
        return self.cdbpool.runQuery(query)
    def populate_cus_list(self, result):
        def formatid(value):
            if value < 10:
                value = '000'+ str(value)
            elif value < 100:
                value = '00'+str(value)
            else:
                value = '0'+str(value)
            return value
        for id, f_name, s_name, l_name, phone, email, meter, line, account in result:
            index = self.clist.InsertStringItem(sys.maxint, str(formatid(id)))
            self.clist.SetStringItem(index, 1, str(f_name))
            self.clist.SetStringItem(index, 2, str(s_name))
            self.clist.SetStringItem(index, 3, str(l_name))
            self.clist.SetStringItem(index, 4, str(phone))
            self.clist.SetStringItem(index, 5, str(email))
            self.clist.SetStringItem(index, 6, str(meter))
            self.clist.SetStringItem(index, 7, str(line))
            self.clist.SetStringItem(index, 8, str(account))
class Chats:
    def __init__(self, parent):
      pass
if __name__ == '__main__':
    app = wx.App()
    app.MainLoop()
