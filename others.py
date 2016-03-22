#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      Nganj
#
# Created:     29/11/2015
# Copyright:   (c) Nganj 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import wx
import os
import hashlib
import time
import datetime
import sys
import MySQLdb as sqldb
def hash(password):
    return hashlib.md5(password).hexdigest()
class Others(wx.Frame):
    def __init__(self, parent, id, choicetable, otherdbpool):
        self.choicetable = choicetable
        wx.Frame.__init__(self, parent, id, 'Displaying '+self.choicetable, size=(1200,500), style=wx.DEFAULT_FRAME_STYLE)
        path = os.path.abspath("./Imagesm/meter.png")
        icon = wx.Icon(path, wx.BITMAP_TYPE_PNG)
##        self.mode = mode

        self.SetIcon(icon)
        self.otherdbpool = otherdbpool
        self.columnname = None
        self.posname = None
        self.tableindb = None
        self.status = 'Inserting'
        self.query = None
        otherparentPanel = wx.Panel(self, -1, size= (-1,-1))
        othervsizer = wx.BoxSizer(wx.VERTICAL)

        self.table = ['Agents', 'Company', 'Meter', 'Position', 'sublocation', 'Location', 'Accounts']
        self.bttnPanel = wx.Panel(otherparentPanel, -1, size=(-1,-1))
        self.tbl = None
        listhsizer = wx.BoxSizer(wx.HORIZONTAL)
        '''Dont iniliase list control, top panel and buttons when company table is selected'''
        newtopPanel  = wx.Panel(otherparentPanel, -1, size=(-1, -1))
        newtopPanel.SetBackgroundColour('green')

        if self.choicetable != 'Company':

            self.dlg = wx.Dialog(self, -1, 'Enter new '+self.choicetable, size=(750, 350))
            self.otherlist = wx.ListCtrl(self.bttnPanel, -1, style= wx.LC_REPORT)
##            tcbttn = wx.Button(ttoppanel, -1, 'Cancel')
##            thsizer.Add(tcbttn, 0, wx.EXPAND|wx.ALL, 5)
            htopsizer = wx.BoxSizer(wx.HORIZONTAL)

            listhsizer.Add(self.otherlist, 1, wx.EXPAND|wx.ALL, 5)
            saveButton = wx.Button(newtopPanel, -1, " Add ", (50, 20))
            refreshBtn = wx.Button(newtopPanel, -1, "Refresh", (50, 20))
            cancelButton = wx.Button(newtopPanel, -1, " Cancel ", (50, 20))
            self.Bind(wx.EVT_BUTTON, self.OnRefresh, id=refreshBtn.GetId())
            self.Bind(wx.EVT_BUTTON, self.OnCancel, id = cancelButton.GetId())

            htopsizer.Add(saveButton, 0, wx.EXPAND | wx.ALL, 5)
            htopsizer.Add(refreshBtn, 0, wx.EXPAND | wx.ALL, 5)
            htopsizer.Add(cancelButton, 0, wx.EXPAND | wx.ALL, 5)
            newtopPanel.SetSizer(htopsizer)

        self.bttnPanel.SetSizer(listhsizer)
        '''chooses table to display'''
        if self.choicetable ==  "Position":
            self.query = """select position, position_desc from position"""
            pq = self.GetList(self.query)
            pq.addCallback(self.OnPosition)
            self.tbl = Position(self.otherdbpool, '', self.status)
            self.Bind(wx.EVT_BUTTON, self.tbl.Displaydlg, id = saveButton.GetId())
        elif self.choicetable == 'Company':
            thsizer = wx.BoxSizer(wx.HORIZONTAL)
            ttoppanel = wx.Panel(otherparentPanel, -1, size=(-1, 100))
            ttoppanel.SetBackgroundColour(wx.BLUE)
            tsbttn = wx.Button(ttoppanel, -1, 'Save')
            thsizer.Add(tsbttn, 0, wx.EXPAND|wx.ALL, 5)
            ttoppanel.SetSizer(thsizer)
            othervsizer.Add(ttoppanel, 0, wx.EXPAND)
            self.tbl = Company(self.otherdbpool, newtopPanel, self.bttnPanel)
            self.Bind(wx.EVT_BUTTON, self.tbl.saveCompany, id=tsbttn.GetId())
        elif self.choicetable == "Agents":
            self.query = """select a.user_id, a.username, b.f_name, b.s_name from credentials a left join employees b on a.user_id =  b.credentials_user_id"""
            pq = self.GetList(self.query)
            pq.addCallback(self.OnAgents)
            self.tbl = Agents(self.otherdbpool, '', self.status)
            self.Bind(wx.EVT_BUTTON, self.tbl.DisplayAgents, id = saveButton.GetId())
        elif self.choicetable == 'Meter':
            self.tbl = Meter(self.otherlist, self.dlg)
            self.Bind(wx.EVT_BUTTON, self.tbl.editMeter, id = saveButton.GetId())
        elif self.choicetable == 'Location':
            self.query = """select a.location_id, a.location, a.Description from location a """
            pq = self.GetList(self.query)
            pq.addCallback(self.OnLocation)
            self.tbl = Location(self.otherdbpool, '', self.status)
            self.Bind(wx.EVT_BUTTON, self.tbl.DisplayLocation, id = saveButton.GetId())
        elif self.choicetable == 'sublocation':
            self.query = """select  a.sub_id, a.line_name, b.location, a.Description from sublocation a inner join location b on b.location_id = a.location_location_id"""
            pq = self.GetList(self.query)
            pq.addCallback(self.OnSublocation)
            self.tbl = sublocation(self.otherdbpool, '', self.status)
            self.Bind(wx.EVT_BUTTON, self.tbl.DisplaySublocation, id = saveButton.GetId())
        elif self.choicetable == 'Accounts':
            self.query = """select a.acc_id, a.account_no, b.f_name, b.s_name, a.Description from accounts a left join clients b on a.acc_id = b.accounts_off"""
            pq = self.GetList(self.query)
            pq.addCallback(self.OnAccounts)
            self.tbl = Accounts(self.otherdbpool, '', self.status)
            self.Bind(wx.EVT_BUTTON, self.tbl.DisplayAccounts, id = saveButton.GetId())
        elif self.choicetable == "Customers":
            self.query = """ select a.client_id, a.f_name, a.s_name, a.l_name, a.phone, a.email, b.meter_no, c.line_name, d.account_no from clients a left join meter b on a.meter_meter_id = b.meter_id left join sublocation c on a.subloc_fgn = c.sub_id left join accounts d on a.accounts_off = d.acc_id"""
            pq = self.GetList(self.query)
            pq.addCallback(self.OnCustomers)
            self.tbl = Customers(self.otherdbpool, '', self.status)
            self.Bind(wx.EVT_BUTTON, self.tbl.DisplayCustomers, id = saveButton.GetId())
        else:
            wx.MessageBox('Invalid error', 'Error', style=wx.ICON_ERROR)

        othervsizer.Add(newtopPanel, 0, wx.EXPAND)
        othervsizer.Add(self.bttnPanel, 1, wx.EXPAND | wx.ALL, 5)
        otherparentPanel.SetSizer(othervsizer)
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        self.Show()
        self.Center()
    def OnPosition(self, result):
        self.posname = None
        self.columnname = 'position'
        self.tableindb = self.choicetable
        self.otherlist.ClearAll()
        self.otherlist.InsertColumn(0, 'Position', width=250)
        self.otherlist.InsertColumn(1, 'Description', wx.LIST_FORMAT_RIGHT, 250)
        for pos, desc in result:
                index = self.otherlist.InsertStringItem(sys.maxint, str(pos))
                self.otherlist.SetStringItem(index, 1, str(desc))
        self.popupmenu = wx.Menu()

        self.otherlist.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.otherlist)
        edit = self.popupmenu.Append(1, 'Edit')
        deletes = self.popupmenu.Append(2, 'Delete')
        self.otherlist.Bind(wx.EVT_MENU, self.EditItemSelected, edit)
        self.otherlist.Bind(wx.EVT_MENU, self.DeleteItemSelected, deletes)
        self.otherlist.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightClickItem, self.otherlist)

    def OnAgents(self, result):
        self.userid = None
        self.columnname = 'user_id'
        self.tableindb = 'Credentials'
        self.otherlist.ClearAll()
        self.otherlist.InsertColumn(0, 'User Id', width=100)
        self.otherlist.InsertColumn(1, 'Username', width=130)
        self.otherlist.InsertColumn(2, 'First Name', width=160)
        self.otherlist.InsertColumn(3, 'Second Name', width =180)
        def formatid(value):
            if value < 10:
                value = '000'+ str(value)
            elif value < 100:
                value = '00'+str(value)
            else:
                value = '0'+str(value)
            return value
        for idname, username, fname, sname in result:
            index = self.otherlist.InsertStringItem(sys.maxint, str(formatid(idname)))
            self.otherlist.SetStringItem(index, 1, str(username))
            self.otherlist.SetStringItem(index, 2, str(fname))
            self.otherlist.SetStringItem(index, 3, str(sname))

        self.popupmenu = wx.Menu()
        edit = self.popupmenu.Append(1, 'Edit')
        deletes = self.popupmenu.Append(2, 'Delete')
        self.otherlist.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.otherlist)
        self.otherlist.Bind(wx.EVT_MENU, self.EditItemSelected, edit)
        self.otherlist.Bind(wx.EVT_MENU, self.DeleteItemSelected, deletes)
        self.otherlist.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightClickItem, self.otherlist)
    def OnLocation(self, result):
        self.userid = None
        self.columnname = 'location_id'
        self.tableindb = self.choicetable
        self.otherlist.ClearAll()
        self.otherlist.InsertColumn(0, 'Area Index', width=140)
        self.otherlist.InsertColumn(1, 'Area', width=140)
        self.otherlist.InsertColumn(2, 'Description', wx.LIST_FORMAT_RIGHT, 270)
        def formatid(value):
            if value < 10:
                value = '000'+ str(value)
            elif value < 100:
                value = '00'+str(value)
            else:
                value = '0'+str(value)
            return value
        for id, area, desc in result:
            index = self.otherlist.InsertStringItem(sys.maxint, str(formatid(id)))
            self.otherlist.SetStringItem(index, 1, str(area))
            self.otherlist.SetStringItem(index, 2, str(desc))
        self.popupmenu = wx.Menu()
        self.otherlist.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.otherlist)
        edit = self.popupmenu.Append(1, 'Edit')
        deletes = self.popupmenu.Append(2, 'Delete')
        self.otherlist.Bind(wx.EVT_MENU, self.EditItemSelected, edit)
        self.otherlist.Bind(wx.EVT_MENU, self.DeleteItemSelected, deletes)
        self.otherlist.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightClickItem, self.otherlist)
    def OnSublocation(self, result):
        self.userid = None
        self.columnname = 'sub_id'
        self.tableindb = self.choicetable
        self.otherlist.ClearAll()
        self.otherlist.InsertColumn(0, 'Sub-location ID', width=140)
        self.otherlist.InsertColumn(1, 'Sub-location', width=140)
        self.otherlist.InsertColumn(2, 'Location', width=80)
        self.otherlist.InsertColumn(3, 'Description', width=130)
        def formatid(value):
            if value < 10:
                value = '000'+ str(value)
            elif value < 100:
                value = '00'+str(value)
            else:
                value = '0'+str(value)
            return value
        for id, sub, loc, desc in result:
            index = self.otherlist.InsertStringItem(sys.maxint, str(formatid(id)))
            self.otherlist.SetStringItem(index, 1, str(sub))
            self.otherlist.SetStringItem(index, 2, str(loc))
            self.otherlist.SetStringItem(index, 3, str(desc))
        self.popupmenu = wx.Menu()
        self.otherlist.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.otherlist)
        edit = self.popupmenu.Append(1, 'Edit')
        deletes = self.popupmenu.Append(2, 'Delete')
        self.otherlist.Bind(wx.EVT_MENU, self.EditItemSelected, edit)
        self.otherlist.Bind(wx.EVT_MENU, self.DeleteItemSelected, deletes)
        self.otherlist.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightClickItem, self.otherlist)
    def OnAccounts(self, result):
        self.userid = None
        self.columnname = 'acc_id'
        self.tableindb = self.choicetable
        self.otherlist.ClearAll()
        self.otherlist.InsertColumn(0, 'Account Index', width=140)
        self.otherlist.InsertColumn(1, 'Account Name', width=140)
        self.otherlist.InsertColumn(2, 'Owners First Name', wx.LIST_FORMAT_RIGHT, 270)
        self.otherlist.InsertColumn(3, 'Owners Second Name', wx.LIST_FORMAT_RIGHT, 270)
        self.otherlist.InsertColumn(4, 'Description', wx.LIST_FORMAT_RIGHT, 270)
        def formatid(value):
            if value < 10:
                value = '000'+ str(value)
            elif value < 100:
                value = '00'+str(value)
            else:
                value = '0'+str(value)
            return value
        for id, accname, fname, sname, desc in result:
            index = self.otherlist.InsertStringItem(sys.maxint, str(formatid(id)))
            self.otherlist.SetStringItem(index, 1, str(accname))
            self.otherlist.SetStringItem(index, 2, str(fname))
            self.otherlist.SetStringItem(index, 3, str(sname))
            self.otherlist.SetStringItem(index, 4, str(desc))
        self.popupmenu = wx.Menu()
        self.otherlist.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.otherlist)
        edit = self.popupmenu.Append(1, 'Edit')
        deletes = self.popupmenu.Append(2, 'Delete')
        self.otherlist.Bind(wx.EVT_MENU, self.EditItemSelected, edit)
        self.otherlist.Bind(wx.EVT_MENU, self.DeleteItemSelected, deletes)
        self.otherlist.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightClickItem, self.otherlist)
    def OnCustomers(self, result):
        self.userid = None
        self.columnname = 'client_id'
        self.tableindb = 'clients'
        self.otherlist.ClearAll()
        self.otherlist.InsertColumn(0, 'Customer Index', width=120)
        self.otherlist.InsertColumn(1, 'First Name', width=100)
        self.otherlist.InsertColumn(2, 'Second Name', wx.LIST_FORMAT_RIGHT, 120)
        self.otherlist.InsertColumn(3, 'Last Name', wx.LIST_FORMAT_RIGHT, 120)
        self.otherlist.InsertColumn(4, 'Phone', wx.LIST_FORMAT_RIGHT, 100)
        self.otherlist.InsertColumn(5, 'Email', wx.LIST_FORMAT_RIGHT, 100)
        self.otherlist.InsertColumn(6, 'Meter Name', wx.LIST_FORMAT_RIGHT, 120)
        self.otherlist.InsertColumn(7, 'Line Name', wx.LIST_FORMAT_RIGHT, 80)
        self.otherlist.InsertColumn(8, 'Account Name', wx.LIST_FORMAT_RIGHT, 100)
        def formatid(value):
            if value < 10:
                value = '000'+ str(value)
            elif value < 100:
                value = '00'+str(value)
            else:
                value = '0'+str(value)
            return value
        for id, f_name, s_name, l_name, phone, email, meter, line, account in result:
            index = self.otherlist.InsertStringItem(sys.maxint, str(formatid(id)))
            self.otherlist.SetStringItem(index, 1, str(f_name))
            self.otherlist.SetStringItem(index, 2, str(s_name))
            self.otherlist.SetStringItem(index, 3, str(l_name))
            self.otherlist.SetStringItem(index, 4, str(phone))
            self.otherlist.SetStringItem(index, 5, str(email))
            self.otherlist.SetStringItem(index, 6, str(meter))
            self.otherlist.SetStringItem(index, 7, str(line))
            self.otherlist.SetStringItem(index, 8, str(account))
        self.popupmenu = wx.Menu()
        self.otherlist.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.otherlist)
        edit = self.popupmenu.Append(1, 'Edit')
        deletes = self.popupmenu.Append(2, 'Delete')
        self.otherlist.Bind(wx.EVT_MENU, self.EditItemSelected, edit)
        self.otherlist.Bind(wx.EVT_MENU, self.DeleteItemSelected, deletes)
        self.otherlist.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightClickItem, self.otherlist)
    def OnRightClickItem(self, event):
        pos = event.GetPosition()
        pos = self.bttnPanel.ScreenToClient(pos)
        self.otherlist.PopupMenu(self.popupmenu, pos)

    def DeleteItemSelected(self, event):
        dels = self.DeleteItem(self.posname, self.tableindb, self.columnname)
        dels.addCallback(self.successDelete)
        dels.addErrback(self.errDelete)
    def EditItemSelected(self, event):
        self.status = 'Editing'
        if self.choicetable == 'Position':
                self.tbl = Position(self.otherdbpool, self.posname, self.status)
                self.tbl.Displaydlg('None')
        elif self.choicetable == 'Agents':
                self.tbl = Agents(self.otherdbpool, self.posname, self.status)
                self.tbl.DisplayAgents('None')
        elif self.choicetable == 'Location':
            self.tbl = Location(self.otherdbpool, self.posname, self.status)
            self.tbl.DisplayLocation(None)
        elif self.choicetable == 'sublocation':
            self.tbl = sublocation(self.otherdbpool, self.posname, self.status)
            self.tbl.DisplaySublocation(None)
        elif self.choicetable == 'Accounts':
            self.tbl = Accounts(self.otherdbpool, self.posname, self.status)
            self.tbl.DisplayAccounts(None)
        elif self.choicetable == 'Customers':
            self.tbl = Customers(self.otherdbpool, self.posname, self.status)
            self.tbl.DisplayCustomers(None)
        else:
            wx.MessageBox( 'Error accessing table name', 'Checking table name', style = wx.ICON_INFORMATION)
    def errDelete(self, error):
        wx.MessageBox("Unable to delete item beacuse its being used","Delete Error", style = wx.ICON_ERROR)
    def successDelete(self, result):
        wx.MessageBox("Deleted Successfully", 'Success deletion', style=wx.ICON_INFORMATION)
##        query = """select position, position_desc from position"""
##        pq = self.GetList(query)
##        pq.addCallback(self.OnPosition)
##        self.otherlist.RefreshItems()
    def DeleteItem(self, itemname, tablename, columnname):
        dlg = wx.MessageDialog(None, 'Are you sure you want to delete this item ?', 'Delete Item', style = wx.ICON_QUESTION|wx.YES_NO)
        ret = dlg.ShowModal()
        if ret == wx.ID_YES:
            return self.otherdbpool.runOperation("""delete from %s where %s = '%s'"""%(tablename, columnname, itemname))
        else:
            pass
        dlg.Destroy()
    def OnItemSelected(self, event):
        item = event.GetItem()
        self.posname = str(item.GetText())
        return self.posname
    def GetList(self, query):
        self.query = query
        return self.otherdbpool.runQuery(self.query)
    def OnRefresh(self, event):
        pq = self.GetList(self.query)
        if self.choicetable == 'Agents':
            pq.addCallback(self.OnAgents)
        elif self.choicetable == 'Position':
            pq.addCallback(self.OnPosition)
        elif self.choicetable == "Location":
            pq.addCallback(self.OnLocation)
        elif self.choicetable == "sublocation":
            pq.addCallback(self.OnSublocation)
        elif self.choicetable == "Accounts":
            pq.addCallback(self.OnAccounts)
        elif self.choicetable == "Customers":
            pq.addCallback(self.OnCustomers)
        else:
            wx.MessageBox('No table chosen','choose table',wx.ICON_INFORMATION)
    def OnCancel(self, event):
        self.dlg.Destroy()
        self.Destroy()
    def OnExit(self, event):
        if self.choicetable != 'Company':
            self.dlg.Destroy()
        self.Destroy()
class Position:
    def __init__(self, dbconn, posname, status):

        self.dbconn = dbconn
        self.status = status
        self.posname = posname

    def Displaydlg(self, event):
        self.pdlg = wx.Dialog(None, -1, 'Position', size=(400, 300), style=wx.STAY_ON_TOP|wx.DEFAULT_FRAME_STYLE)
        postoppanel = wx.Panel(self.pdlg, -1, size=(-1, 200))
        postoppanel.SetBackgroundColour(wx.GREEN)
        posbttmpanel = wx.Panel(self.pdlg, -1, size=(-1, -1))
        positionTxt = wx.StaticText(posbttmpanel, -1, 'Position:')
        self.positionCtrl = wx.TextCtrl(posbttmpanel, -1, size=(200, -1))
        descTxt =wx.StaticText(posbttmpanel, -1, 'Description:')
        self.descCtrl = wx.TextCtrl(posbttmpanel, -1, size=(200, -1), style=wx.TE_MULTILINE)
        btnSave = wx.Button(postoppanel, -1, ' Save ')
        self.pdlg.Bind(wx.EVT_BUTTON, self.Conundrum, id=btnSave.GetId())
        btnCancel = wx.Button(postoppanel, -1, ' Cancel ')
        self.pdlg.Bind(wx.EVT_BUTTON, self.OnCancel, id=btnCancel.GetId())
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        vsizer= wx.BoxSizer(wx.VERTICAL)
        vsizer1 = wx.BoxSizer(wx.VERTICAL)

        vsizer.Add(positionTxt, 0, wx.EXPAND | wx.ALL, 5)
        vsizer1.Add(self.positionCtrl, 0, wx.EXPAND | wx.ALL, 5)
        vsizer.Add(descTxt, 0, wx.EXPAND | wx.ALL, 5)
        vsizer1.Add(self.descCtrl, 0, wx.EXPAND | wx.ALL, 5)

        hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer2.Add(btnSave, 0, wx.EXPAND | wx.ALL, 5)
        hsizer2.Add(btnCancel, 0, wx.EXPAND | wx.ALL, 5)

        hsizer.Add(vsizer)
        hsizer.Add(vsizer1)

        if self.status == 'Editing':
            self.calledposition = self.getPosition(1)
            self.calledposition.addCallback(self.editPosition)

        postoppanel.SetSizer(hsizer2)
        posbttmpanel.SetSizer(hsizer)
        posvsizer = wx.BoxSizer(wx.VERTICAL)
        posvsizer.Add(postoppanel, 0, wx.EXPAND)
        posvsizer.Add(posbttmpanel, 1, wx.EXPAND | wx.ALL, 5)
        self.pdlg.SetSizer(posvsizer)
        self.pdlg.Bind(wx.EVT_CLOSE, self.OnExit)
        self.pdlg.ShowModal()
        self.pdlg.Destroy()
    def OnExit(self, event):
        self.pdlg.Destroy()
    def Conundrum(self, event):
        self.insertmeth = self.InsertPosition(1)
        self.insertmeth.addCallback(self.OnSaveSuccess)
        self.insertmeth.addErrback(self.OnSaveErr)
    def OnSaveSuccess(self, result):
        if self.status == 'Editing':
            wx.MessageBox('Updated Successfully', '  Success', style=wx.ICON_INFORMATION)
            self.pdlg.Destroy()
        elif self.status == 'Deleting':
            wx.MessageBox('Deleted Successfully', '  Success', style=wx.ICON_INFORMATION)
            self.pdlg.Destroy()
        elif self.status == 'Inserting':
            wx.MessageBox('Inserted Successfully', '  Success', style=wx.ICON_INFORMATION)
            self.pdlg.Destroy()
        else:
            wx.MessageBox('Unknown Error', '  Error', style=wx.ICON_ERROR)
            self.pdlg.Destroy()
    def OnSaveErr(self, error):
        wx.MessageBox('Check if position is already in the system'+str(error),'Duplication error', style=wx.ICON_ERROR)
    def InsertPosition(self, value):
        if self.positionCtrl.GetValue() != None and self.positionCtrl.GetValue() != '':
            if self.status == 'Inserting':
                return self.dbconn.runOperation("""insert into position (position, position_desc) values ( "%s", "%s")"""% (self.positionCtrl.GetValue(), self.descCtrl.GetValue()))
            elif self.status == 'Editing':
                return self.dbconn.runOperation("""update position set position ='%s', position_desc ='%s' where position = '%s'"""%(self.positionCtrl.GetValue(),  self.descCtrl.GetValue(), self.posname))
            elif self.status == 'Deleting':
                dlg = wx.Dialog(None, -1, 'Delete Operation', style= wx.YES_NO)
                qresult = dlg.ShowModal()
                if qresult == wx.ID_YES:
                    return self.dbconn.runOperation("""delete from position where position = '%s'"""%(self.posname))
                else:
                    pass
                dlg.Destroy()
            else:
                wx.MessageBox('Unknown Parameters', 'Parameter Implicit', style= wx.ICON_INFORMATION)
        else:
            wx.MessageBox('Fields dont have values','Field values error', style=wx.ICON_ERROR)
    def editPosition(self, result):
        for pos, desc in result:
            self.positionCtrl.SetValue(str(pos))
            self.descCtrl.SetValue(str(desc))
    def EditErr(self, result):
        wx.MessageBox('Error getting data from database', 'Update Error', wx.ICON_ERROR|wx.STAY_ON_TOP)
    def getPosition(self, values):
        return self.dbconn.runQuery("""select position, position_desc from position where position = '%s'"""%(self.posname))
    def UpdatePosition(self):
        pass
    def OnCancel(self, event):
        self.pdlg.Close()
class Agents:
    def __init__(self, adbconn, aposname, astatus):
        self.adbconn = adbconn
        self.aposname = aposname
        self.astatus = astatus
        self.passwd = None

    def DisplayAgents(self, event):

        self.adlg = wx.Dialog(None, -1, "Agents", size=(800, 400), style=wx.DEFAULT_FRAME_STYLE)
        self.agridsizer = wx.GridBagSizer(vgap=8, hgap=8)
        userpanel = wx.Panel(self.adlg, -1, size=(-1, -1))
        atoppanel = wx.Panel(self.adlg, -1, size=(-1, 200))
        atoppanel.SetBackgroundColour(wx.GREEN)
        usertxt = wx.StaticText(userpanel, -1, "Username:")
        self.userctrl = wx.TextCtrl(userpanel, -1, size=(200, -1))
        oldpasstxt = wx.StaticText(userpanel, -1, 'Old Password:')
        self.oldpassctrl = wx.TextCtrl(userpanel, -1, size=(200, -1), style = wx.TE_PASSWORD)
        self.oldpassctrl.Disable()
        newpasstxt = wx.StaticText(userpanel, -1, 'New Pasword:')
        self.newpassctrl = wx.TextCtrl(userpanel, -1, size=(200, -1), style = wx.TE_PASSWORD)

        confirmpasstxt = wx.StaticText(userpanel, -1, 'Confirm New Pasword:')
        self.confirmpassctrl = wx.TextCtrl(userpanel, -1, size=(200, -1), style = wx.TE_PASSWORD)


        ahsizer =wx.BoxSizer(wx.HORIZONTAL)
        userSavebtn = wx.Button(atoppanel, -1, 'Save')
        atoppanel.Bind(wx.EVT_BUTTON, self.editAgents, id = userSavebtn.GetId())
        userCancelbtn = wx.Button(atoppanel, -1, 'Cancel')
        ahsizer.Add(userSavebtn, 0, wx.EXPAND| wx.ALL, 5)
        ahsizer.Add(userCancelbtn, 0, wx.EXPAND|wx.TOP|wx.RIGHT|wx.BOTTOM, 5)
        self.adlg.Bind(wx.EVT_BUTTON, self.OnCancel, id= userCancelbtn.GetId())
        atoppanel.SetSizer(ahsizer)
        self.agridsizer.Add(usertxt, (1,1), (1, 3))
        self.agridsizer.Add(self.userctrl, (1, 4), (1,3))
        self.agridsizer.Add(oldpasstxt, (1, 8), (1, 3))
        self.agridsizer.Add(self.oldpassctrl, (1, 12 ), (1, 3))

        self.agridsizer.Add(newpasstxt, (2,1), (1, 3))
        self.agridsizer.Add(self.newpassctrl, (2, 4), (1,3))
        self.agridsizer.Add(confirmpasstxt, (2, 8), (1, 3))
        self.agridsizer.Add(self.confirmpassctrl, (2, 12 ), (1, 3))

        if self.astatus == 'Editing':
            self.calledagent = self.GetAgents(1)
            self.calledagent.addCallback(self.SetAgentCtrl)
            self.oldpassctrl.Enable()

        else:
            pass
        userpanel.SetSizer(self.agridsizer)
        avsizer = wx.BoxSizer(wx.VERTICAL)
        avsizer.Add(atoppanel, 0, wx.EXPAND)
        avsizer.Add(userpanel, 1, wx.EXPAND | wx.ALL, 5)
        self.adlg.SetSizer(avsizer)
        self.adlg.ShowModal()
        self.adlg.Destroy()
    def GetAgents(self, jk):
        return self.adbconn.runQuery("""select username, password from credentials where user_id = '%s'"""%(self.aposname))
    def SetAgentCtrl(self, result):
        for username, password in result:
            self.userctrl.SetValue(str(username))
    def editAgents(self, event):
        retrndb = self.GetAgents(1)
        retrndb.addCallback(self.insertAgents)
    def insertAgents(self, result):
        username1 = None
        password1 = None
        for username, password in result:
            username1 = username
            password1 = password
        if self.astatus == 'Editing':
            if self.checkPasswordExistsInDb(password1) == True:
                if self.userctrl.GetValue() != None and self.userctrl.GetValue() != "None" and self.userctrl.GetValue() != '':
                    if self.checkPasswordMatch(1) == True:
                        insertdata = self.StoreInDb("""update credentials  set username = '%s', password = '%s' where user_id = '%s'"""%(self.userctrl.GetValue(), hash(self.newpassctrl.GetValue()), int(self.aposname)))
                        insertdata.addCallback(self.AgentsSuccess)
                        insertdata.addErrback(self.AgentsErr)
                    else:
                        wx.MessageBox('Passwords do not match try again', 'Password Mismatch', style=wx.ICON_ERROR)
                else:
                    wx.MessageBox('Username cannot be empty', 'Username Error', style=wx.ICON_ERROR)
            else:
                wx.MessageBox("Incorrect old pasword", 'Invalid password', style = wx.ICON_ERROR)
        elif self.astatus == "Inserting":
            if self.userctrl.GetValue() != None and self.userctrl.GetValue() != "None" and self.userctrl.GetValue() != '':
                if self.checkPasswordMatch(1) == True:
                    insertdata = self.StoreInDb("""insert into credentials (username, password) values ('%s','%s')"""%(self.userctrl.GetValue(), hash(self.newpassctrl.GetValue())))
                    insertdata.addCallback(self.AgentsSuccess)
                    insertdata.addErrback(self.AgentsErr)
                else:
                    wx.MessageBox('Passwords do not match try again', 'Password Mismatch', style=wx.ICON_ERROR)
        else:
            wx.MessageBox("Unknown error in inserting or updating agents", 'update insert error', style = wx.ICON_ERROR)
    def checkPasswordExistsInDb(self, passwds):
        self.passwd = passwds
        if self.passwd == '' or self.passwd == None:
            if hash(self.passwd) == hash(str(self.oldpassctrl.GetValue())):
                print hash(self.passwd), hash(self.oldpassctrl.GetValue())
                return True
            else:
                return False
        else:
            if self.passwd == hash(str(self.oldpassctrl.GetValue())):
                print self.passwd, hash(self.oldpassctrl.GetValue())
                return True
            else:
                return False
##                wx.MessageBox("Incorrect old pasword", 'Invalid password', style = wx.ICON_ERROR)
    def checkPasswordMatch(self, values):
        if hash(str(self.newpassctrl.GetValue())) == hash(str(self.confirmpassctrl.GetValue())):
            return True
        else:
            return False
##            wx.MessageBox('Passwords do not match try again', 'Password Mismatch', style=wx.ICON_ERROR)
    def StoreInDb(self, query):
        return self.adbconn.runOperation(query)
    def AgentsSuccess(self, success):
        wx.MessageBox('Operation successfully', 'Success', wx.ICON_INFORMATION)
    def AgentsErr(self, err):
        wx.MessageBox("A database error has occurred, check if your duplicating item", 'Database error', style = wx.ICON_ERROR)
    def OnCancel(self, event):
        self.adlg.Close()
class Company:
    def __init__(self, codbpool, tpanel, bpanel):
        self.tpanel = tpanel
        self.bpanel = bpanel
        self.codbpool = codbpool
        self.d = self.connect(1)

##        dlgco = wx.Dialog(None, -1, 'Company', size=(900, 400))
##        self.bpanel = wx.Panel(self.bpanel, -1, (-1, -1))
##        toppanel = wx.Panel(self.tpanel, -1, (-1, 320))
##        toppanel.SetBackgroundColour(wx.GREEN)
        mainvzr = wx.BoxSizer(wx.VERTICAL)
        topgridbag = wx.GridBagSizer(vgap=5, hgap=5)
        cogridbag = wx.GridBagSizer(vgap=5, hgap=5)
        imgpath = './Imagesm/sys/company.png'
        self.imgCoPanel = wx.Panel(self.tpanel, size=(80, 80))
        self.img = wx.Image(imgpath, type=wx.BITMAP_TYPE_ANY, index=-1)
        wx.StaticBitmap(self.imgCoPanel, -1, wx.BitmapFromImage(self.img))
        self.imgCoPanel.SetBackgroundColour(wx.GREEN)

        self.regNumbertxt = wx.StaticText(self.tpanel, -1, "Registration Number:")
        self.regNumberctrl = wx.TextCtrl(self.tpanel, -1, size=(350, -1))
        self.conametxt = wx.StaticText(self.tpanel, -1, "Company Name:")
        self.conamectrl = wx.TextCtrl(self.tpanel, -1, size=(600, -1))
        self.emptytxt =wx.StaticText(self.tpanel, -1, '')

        self.cophonetxt = wx.StaticText(self.bpanel, -1, "Phone:")
        self.cophonectrl = wx.TextCtrl(self.bpanel, -1, size=(200, -1))
        self.comobiletxt = wx.StaticText(self.bpanel, -1, "Mobile:")
        self.comobilectrl = wx.TextCtrl(self.bpanel, -1, size=(200, -1))
        self.cofaxtxt = wx.StaticText(self.bpanel, -1, "Fax:")
        self.cofaxctrl = wx.TextCtrl(self.bpanel, -1, size=(200, -1))
        self.cowebsitetxt = wx.StaticText(self.bpanel, -1, "Website:")
        self.cowebsitectrl = wx.TextCtrl(self.bpanel, -1, size=(200, -1))
        self.coemailtxt = wx.StaticText(self.bpanel, -1, "Email:")
        self.coemailctrl = wx.TextCtrl(self.bpanel, -1, size=(200, -1))
        self.coCountrytxt = wx.StaticText(self.bpanel, -1, "Country:")
        self.coCountryctrl = wx.TextCtrl(self.bpanel, -1, size=(200, -1))
        self.cocitytxt = wx.StaticText(self.bpanel, -1, "City:")
        self.cocityctrl = wx.TextCtrl(self.bpanel, -1, size=(200, -1))
        self.copostaltxt = wx.StaticText(self.bpanel, -1, "Postal Box:")
        self.copostalctrl = wx.TextCtrl(self.bpanel, -1, size=(200, -1))
        self.costreet1txt = wx.StaticText(self.bpanel, -1, "Street 1:")
        self.costreet1ctrl = wx.TextCtrl(self.bpanel, -1, size=(200, -1))
        self.postalcodetxt = wx.StaticText(self.bpanel, -1, "Postal Code:")
        self.postalcodectrl = wx.TextCtrl(self.bpanel, -1, size=(200, -1))
        self.codatecreatedtxt = wx.StaticText(self.bpanel, -1, "Date of Creation:")
        self.codatecreateddpc = wx.DatePickerCtrl(self.bpanel, size=(120,-1), style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY | wx.DP_ALLOWNONE | wx.ALIGN_RIGHT,  )
        self.cosavebtn = wx.Button(bpanel, -1, " Edit ")
##        cocancelbtn = wx.Button(bpanel, -1, " Cancel ")

        topgridbag.Add(self.imgCoPanel, (1, 1), (3, 2))
        topgridbag.Add(self.regNumbertxt, (1, 3), (1, 2))
        topgridbag.Add(self.regNumberctrl, (1, 6), (1, 3))
        topgridbag.Add(self.conametxt, (2, 3), (1,2))
        topgridbag.Add(self.conamectrl, (2, 6), (1, 5))
        topgridbag.Add(self.emptytxt, (4, 1), (1, 3))
        self.tpanel.SetSizer(topgridbag)

        cogridbag.Add(self.cophonetxt, (1, 1), (1, 3))
        cogridbag.Add(self.cophonectrl, (1, 4), (1, 3))
        cogridbag.Add(self.costreet1txt, (1, 8), (1, 3))
        cogridbag.Add(self.costreet1ctrl, (1, 12), (1, 3))
        cogridbag.Add(self.comobiletxt, (2, 1), (1, 3))
        cogridbag.Add(self.comobilectrl, (2, 4), (1, 3))
        cogridbag.Add(self.postalcodetxt, (2, 8), (1, 3))
        cogridbag.Add(self.postalcodectrl, (2, 12), (1, 3))

        cogridbag.Add(self.copostaltxt, (3, 1), (1, 3))
        cogridbag.Add(self.copostalctrl, (3, 4), (1, 3))
        cogridbag.Add(self.cofaxtxt, (3, 8), (1, 3))
        cogridbag.Add(self.cofaxctrl, (3, 12), (1, 3))

        cogridbag.Add(self.coemailtxt, (4, 1), (1, 3))
        cogridbag.Add(self.coemailctrl, (4, 4), (1, 3))
        cogridbag.Add(self.cocitytxt, (4, 8), (1, 3))
        cogridbag.Add(self.cocityctrl, (4, 12), (1, 3))
        cogridbag.Add(self.cowebsitetxt, (5, 1), (1, 3))
        cogridbag.Add(self.cowebsitectrl, (5, 4), (1, 3))
        cogridbag.Add(self.coCountrytxt, (5, 8), (1, 3))
        cogridbag.Add(self.coCountryctrl, (5, 12), (1, 3))
        cogridbag.Add(self.codatecreatedtxt, (6, 1), (1, 3))
        cogridbag.Add(self.codatecreateddpc, (6, 4), (1, 3))
        cogridbag.Add(self.cosavebtn, (9, 1),(1, 3))
        self.company_columns = ['co_id','reg_no','co_name', 'co_pstl_addr','postal_code','co_tel_1' ,'mobile' ,'co_email','website' ,'dateofcreation','fax','city','country', 'street',]
        self.company_data = ['id', 'self.regNumberctrl', 'self.conamectrl', 'self.copostalctrl', 'self.postalcodectrl', 'self.cophonectrl', 'self.comobilectrl', 'self.coemailctrl', 'self.cowebsitectrl', 'self.codatecreateddpc','self.cofaxctrl', 'self.cocityctrl', 'self.coCountryctrl', 'self.costreet1ctrl']
        self.d.addCallback(self.printRecs)
##        cogridbag.Add(cocancelbtn, (9, 4), (1,3))
        self.bpanel.Bind(wx.EVT_BUTTON, self.editCompany, id = self.cosavebtn.GetId())
        self.bpanel.SetSizer(cogridbag)
    def onCancel(self, event):
        self.Destroy()
    def editCompany(self,  event):
        for cols in range(0, len(self.company_data)):
            colname = eval(self.company_data[cols])
            if cols == 0:
                pass
            else:
                colname.Enable()
    def saveCompany(self, event):
        table = 'company'
        try:
            for col in range(0, len(self.company_data)):
                col_name = eval(self.company_data[col])
                if col == 0:
                    pass
                elif self.company_data[col] == 'self.codatecreateddpc':
                    date_data = col_name.GetValue()
                    g, l = str(date_data).split(' ')
                    m, d, yr = g.split('/')
                    minutes, sec, milsec = l.split(':')
                    today_day = str(datetime.datetime.today())
                    split_today = today_day.split(' ')
                    last_digit = split_today[0]
                    def daterange(year):
                        if int(year) in range(70, 100):
                            year = '19' + year
                        elif int(year) in range(1, int(last_digit[-2:])+1):
                            year = '20'+ year
                        else:
                            yeardlg = wx.MessageDialog(None, 'Date not within range','Date Warning', style=wx.OK|wx.ICON_ERROR)
                            yeardlg.ShowModal()
                            yeardlg.Destroy()
                        return int(year)

                    date_in_sec =(datetime.datetime(daterange(yr),int(m), int(d), int(minutes), int(sec), int(milsec)) - datetime.datetime(1970,1,1)).total_seconds()
                    try:
                        self.codbpool.runOperation("""update %s set  %s='%f' where co_id = 1;""" %\
                         (table, self.company_columns[col], date_in_sec))
                    except Exception:
                        dlg1 = wx.MessageDialog(None, 'Error while updating Date', 'Warning',style= wx.ICON_ERROR|wx.OK)
                        dlg1.ShowModal()
                        dlg1.Destroy()

                elif col_name.GetValue() == '':
                    pass
                else:
                    db_data = col_name.GetValue()
                    try:
                        self.codbpool.runOperation("""update %s set  %s='%s' where co_id = 1;""" %\
                         (table, self.company_columns[col], db_data))
                    except Exception:
                        dlg1 = wx.MessageDialog(None, 'Error while updating', 'Warning',style= wx.ICON_ERROR|wx.OK)
                        dlg1.ShowModal()
                        dlg1.Destroy()
        except Exception :
            dlg2 = wx.MessageDialog(None, 'General error, an error occured when updating', 'Warning',style= wx.ICON_ERROR|wx.OK)
            dlg2.ShowModal()
            dlg2.Destroy()
    def connect(self, var):
        new = self.codbpool.runQuery('select * from company')
        return new
    def printRecs(self, results):
        j = 0
        for i in results:
            for item in i:
                ctrl = eval(self.company_data[j])

                if j == 0:
                    pass
                else:
                    if item == None:
                        ctrl.Disable()
                        pass
                    elif self.company_data[j] == 'self.codatecreateddpc':
                        c_date = datetime.date.fromtimestamp(item)
                        new_date = str(c_date)
                        y, m ,d = new_date.split('-')
                        dt = wx.DateTimeFromDMY(int(d), int(m), int(y))
                        ctrl.SetValue(dt)
                        ctrl.Disable()
                    else:
                        ctrl.AppendText(str(item))
                        ctrl.Disable()
                j += 1
##        print self.codatecreateddpc.GetValue()
##            l = 0
##            for z in i:
##                self.company_data[self.company_columns[l]] = z
##                l += 1
##            print self.company_data
##            self.regNumberctrl.SetT

class Meter:
    def __init__(self, mlist, mdlg):
        meters = [('7783647365','James Manungu','Muchatha'),('129373653','Hunk niut','Karuri')]
        self.mlist = mlist
        self.mdlg = mdlg
        self.mlist.InsertColumn(0, "Meter Number", width=100)
        self.mlist.InsertColumn(1,  "Full name", width=100)
        self.mlist.InsertColumn(2, "Locality", width=100)
        for i in meters:
            index = self.mlist.InsertStringItem(sys.maxint, i[0])
            self.mlist.SetStringItem(index, 1, i[1])
            self.mlist.SetStringItem(index, 2, i[2])

    def editMeter(self, event):
        mtoppanel = wx.Panel(self.mdlg, -1, size=(-1, 250))
        mtoppanel.SetBackgroundColour(wx.GREEN)
        msavebtn =wx.Button(mtoppanel, -1, " Save ")
        mcancelbtn = wx.Button(mtoppanel, -1, " Cancel ")
        mbelowpanel = wx.Panel(self.mdlg, -1, size=(-1,-1))
        mmetertxt = wx.StaticText(mbelowpanel, -1, "Meter Number:")
        mmeterctrl = wx.TextCtrl(mbelowpanel, -1, size=(200, -1))
        mhtopsizer = wx.BoxSizer(wx.HORIZONTAL)
        mhbottomsizer = wx.BoxSizer(wx.HORIZONTAL)
        mhtopsizer.Add(msavebtn, 0, wx.EXPAND | wx.ALL, 5)
        mhtopsizer.Add(mcancelbtn, 0 , wx.EXPAND| wx.ALL, 5)
        self.mdlg.Bind(wx.EVT_BUTTON, self.OnCancel, id=mcancelbtn.GetId())
        mtoppanel.SetSizer(mhtopsizer)
        mhbottomsizer.Add(mmetertxt, 0, wx.ALL, 5)
        mhbottomsizer.Add(mmeterctrl, 0, wx.ALL, 5)
        mbelowpanel.SetSizer(mhbottomsizer)
        mvsizer = wx.BoxSizer(wx.VERTICAL)
        mvsizer.Add(mtoppanel, 0, wx.EXPAND)
        mvsizer.Add(mbelowpanel, 1, wx.EXPAND)
        self.mdlg.SetSizer(mvsizer)
        self.mdlg.ShowModal()
    def OnCancel(self, event):
        self.mdlg.Close()

class sublocation:
    def __init__(self, subdbconn, subposname, substatus):
        self.subdbconn = subdbconn
        self.subposname = subposname
        self.substatus  = substatus
        self.combolist = []
    def DisplaySublocation(self, event):
        self.sdlg = wx.Dialog(None, -1, 'Enter New Sub-Location', size=(750, 350))
        stoppanel = wx.Panel(self.sdlg, -1, size=(-1, 250))
        stoppanel.SetBackgroundColour(wx.GREEN)
        ssavebtn =wx.Button(stoppanel, -1, " Save ")
        scancelbtn = wx.Button(stoppanel, -1, " Cancel ")
        self.sdlg.Bind(wx.EVT_BUTTON, self.OnCancel, id=scancelbtn.GetId())
        self.sdlg.Bind(wx.EVT_BUTTON, self.OnSave, id=ssavebtn.GetId())
        shsizer = wx.BoxSizer(wx.HORIZONTAL)
        shsizer.Add(ssavebtn, 0, wx.EXPAND| wx.ALL, 5)
        shsizer.Add(scancelbtn, 0, wx.EXPAND| wx.ALL, 5)
        stoppanel.SetSizer(shsizer)
        sgsizer = wx.GridBagSizer(vgap=5, hgap=5)
        sbottonpnl = wx.Panel(self.sdlg, -1, size=(-1,-1))
        slocationtxt = wx.StaticText(sbottonpnl, -1, 'Location:')

        self.slocationctrl = wx.ComboBox(sbottonpnl, -1, choices = [], style= wx.CB_READONLY)
        g = self.QueryDb("""select location from location""")
        g.addCallback(self.SetComboItems)
        ssubloctxt = wx.StaticText(sbottonpnl, -1, "Sublocation:")
        self.ssublocctrl = wx.TextCtrl(sbottonpnl, -1, size=(200, -1))
        sdesctxt = wx.StaticText(sbottonpnl, -1, "Description:")
        self.sdescctrl = wx.TextCtrl(sbottonpnl, -1, size=(200, -1))

        sgsizer.Add(slocationtxt, (1,1), (1, 3))
        sgsizer.Add(self.slocationctrl, (1, 4), (1, 3))
        sgsizer.Add(ssubloctxt, (2, 1), (1, 3))
        sgsizer.Add(self.ssublocctrl, (2, 4), (1, 3))
        sgsizer.Add(sdesctxt, (3, 1), (1,3))
        sgsizer.Add(self.sdescctrl, (3, 4), (1, 3))
        if self.substatus == 'Editing':
            gt = self.GetSubLocation()
            gt.addCallback(self.SetData)
        sbottonpnl.SetSizer(sgsizer)
        svsizer = wx.BoxSizer(wx.VERTICAL)
        svsizer.Add(stoppanel, 0, wx.EXPAND)
        svsizer.Add(sbottonpnl, 1, wx.EXPAND)

        self.sdlg.SetSizer(svsizer)
        self.sdlg.ShowModal()
        self.sdlg.Destroy()
    def SetComboItems(self, results):
        for i in results:
            self.combolist.append(i[0])
        self.slocationctrl.SetItems(self.combolist)
    def GetSubLocation(self):
        return self.QueryDb("""select  a.sub_id, a.line_name, b.location, a.Description from sublocation a inner join location b on b.location_id = a.location_location_id where sub_id = '%s'"""%(self.subposname))
    def SetData(self, result):
        for sub_id, line_name, location, description in result:
            self.slocationctrl.SetValue(str(location))
            self.ssublocctrl.SetValue(str(line_name))
            if str(description) != 'None':
                self.sdescctrl.SetValue(str(description))
    def UpdateSubLocation(self):
        if self.slocationctrl.GetValue() == None or self.slocationctrl.GetValue() == '' or self.slocationctrl.GetValue() == 'None' or self.ssublocctrl == None:
            wx.MessageBox(' Warning, fields cannot be empty', ' Warning', wx.ICON_WARNING)
        else:
            return self.QueryDb(""" update sublocation set line_name ='%s', location_location_id = (select location_id from location where location = '%s'), Description='%s' where sub_id = '%s'"""%(str(self.ssublocctrl.GetValue()), str(self.slocationctrl.GetValue()), str(self.sdescctrl.GetValue()),str(self.subposname)))
    def InsertSubLocation(self):
        if self.slocationctrl.GetValue() == None or self.slocationctrl.GetValue() == '' or self.slocationctrl.GetValue() == 'None' or self.ssublocctrl == None:
            wx.MessageBox(' Warning, fields cannot be empty', ' Warning', wx.ICON_WARNING)
        else:
            return self.QueryDb("""insert into sublocation (line_name, location_location_id, Description) values ('%s',(select location_id from location where location = "%s"), '%s')"""%(str(self.ssublocctrl.GetValue()), str(self.slocationctrl.GetStringSelection()),  str(self.sdescctrl.GetValue())))
    def OnSave(self, event):
        if self.substatus == 'Editing':
            update = self.UpdateSubLocation()
            update.addCallback(self.OnSuccess)
            update.addErrback(self.OnErr)
        else:
            insert = self.InsertSubLocation()
            insert.addCallback(self.OnSuccess)
            insert.addErrback(self.OnErr)
    def QueryDb(self, query):
        return self.subdbconn.runQuery(query)
    def OnSuccess(self, result):
        wx.MessageBox('Operation Successful', ' Operation info', wx.ICON_INFORMATION)
        self.sdlg.Destroy()
    def OnErr(self, err):
        wx.MessageBox('Operation Failed '+str(err),' Operation info', wx.ICON_ERROR)
    def OnCancel(self, event):
        self.sdlg.Close()
class Location:
    def __init__(self, ldbconn, lposname, lstatus):
        self.ldbconn = ldbconn
        self.lposname = lposname
        self.lstatus = lstatus
    def DisplayLocation(self, event):
        self.ldlg = wx.Dialog(None, -1, 'Enter New Location', size=(750, 350))
        ltoppanel = wx.Panel(self.ldlg, -1, size=(-1, 250))
        ltoppanel.SetBackgroundColour(wx.GREEN)
        lsavebtn = wx.Button(ltoppanel, -1, " Save ")
        lcancelbtn = wx.Button(ltoppanel, -1, " Cancel ")
        lbelowpanel = wx.Panel(self.ldlg, -1, size=(-1,-1))
        lnametxt = wx.StaticText(lbelowpanel, -1, "Location:")
        self.lctrl = wx.TextCtrl(lbelowpanel, -1, size=(200, -1))
        ldesctxt = wx.StaticText(lbelowpanel, -1, "Description:")
        self.ldescctrl = wx.TextCtrl(lbelowpanel, -1, size=(200, -1), style= wx.TE_MULTILINE)
        self.ldlg.Bind(wx.EVT_BUTTON, self.OnSave, id=lsavebtn.GetId())
        self.ldlg.Bind(wx.EVT_BUTTON, self.OnCancel, id=lcancelbtn.GetId())

        lhtopsizer = wx.BoxSizer(wx.HORIZONTAL)

        lhbottomsizer = wx.BoxSizer(wx.VERTICAL)
        lhbottomsizer1 = wx.BoxSizer(wx.VERTICAL)

        lhtopsizer.Add(lsavebtn, 0, wx.EXPAND | wx.ALL, 5)
        lhtopsizer.Add(lcancelbtn, 0 , wx.EXPAND | wx.ALL, 5)
        ltoppanel.SetSizer(lhtopsizer)

        lhbottomsizer.Add(lnametxt, 0,  wx.EXPAND | wx.ALL, 5)
        lhbottomsizer1.Add(self.lctrl, 0,   wx.EXPAND | wx.ALL, 5)
        lhbottomsizer.Add(ldesctxt, 0,    wx.EXPAND | wx.ALL, 5)
        lhbottomsizer1.Add(self.ldescctrl, 0,   wx.EXPAND | wx.ALL, 5)

        lbttmvsizer = wx.BoxSizer(wx.HORIZONTAL)
        lbttmvsizer.Add(lhbottomsizer, 0, wx.EXPAND |wx.ALL, 5)
        lbttmvsizer.Add(lhbottomsizer1, 0, wx.EXPAND |wx.ALL, 5)

        lbelowpanel.SetSizer(lbttmvsizer)
        lvsizer = wx.BoxSizer(wx.VERTICAL)
        lvsizer.Add(ltoppanel, 0, wx.EXPAND)
        lvsizer.Add(lbelowpanel, 1, wx.EXPAND)
        if self.lstatus == 'Editing':
            newids = self.GetLocation()
            newids.addCallback(self.SetData)
        self.ldlg.SetSizer(lvsizer)
        self.ldlg.ShowModal()
        self.ldlg.Destroy()
    def GetLocation(self):
        return self.StoreIntoDb("""select location_id, location, Description from Location where location_id='%s'"""%(self.lposname))
    def SetData(self, result):
        for id, location, description in result:
            self.lctrl.SetValue(str(location))
            if str(description) != 'None':
                self.ldescctrl.SetValue(str(description))
    def UpdateLocation(self):
        if self.lctrl.GetValue() == None or self.lctrl.GetValue() == '' or self.lctrl.GetValue() == 'None':
            wx.MessageBox(' Warning, fields cannot be empty', ' Warning', wx.ICON_WARNING)
        else:
            return self.StoreIntoDb(""" update location set location ='%s', Description='%s' where location_id = '%s'"""%(str(self.lctrl.GetValue()), str(self.ldescctrl.GetValue()), str(self.lposname)))
    def InsertLocation(self):
        if self.lctrl.GetValue() == None or self.lctrl.GetValue() == '' or self.lctrl.GetValue() == 'None':
            wx.MessageBox(' Warning, fields cannot be empty', ' Warning', wx.ICON_WARNING)
        else:
            return self.StoreIntoDb("""insert into location (location, Description) values ('%s', '%s')"""%(str(self.lctrl.GetValue()), str(self.ldescctrl.GetValue())))
    def OnSave(self, event):
        if self.lstatus == 'Editing':
            update = self.UpdateLocation()
            update.addCallback(self.OnSuccess)
            update.addErrback(self.OnErr)
        else:
            insert = self.InsertLocation()
            insert.addCallback(self.OnSuccess)
            insert.addErrback(self.OnErr)
    def StoreIntoDb(self, query):
        return self.ldbconn.runQuery(query)
    def OnSuccess(self, result):
        wx.MessageBox('Operation Successful', ' Operation info', wx.ICON_INFORMATION)
        self.ldlg.Destroy()
    def OnErr(self, err):
        wx.MessageBox('Operation Failed '+ str(err), ' Operation info', wx.ICON_ERROR)
    def OnCancel(self, event):
        self.ldlg.Destroy()

class Accounts:
    def __init__(self, accdbconn, accposname, accstatus):
        self.accdbconn = accdbconn
        self.accposname =  accposname
        self.accstatus = accstatus
    def DisplayAccounts(self, event):
        self.accdlg = wx.Dialog(None, -1, 'Enter New Account', size=(750, 350))
        atoppnl = wx.Panel(self.accdlg, -1)
        abottmpnl = wx.Panel(self.accdlg, -1)
        atoppnl.SetBackgroundColour(wx.GREEN)
        asavebtn =wx.Button(atoppnl, -1, " Save ")
        acancelbtn = wx.Button(atoppnl, -1, " Cancel ")
        ametertxt = wx.StaticText(abottmpnl, -1, "Account Number:")
        self.accctrl = wx.TextCtrl(abottmpnl, -1, size=(200, 30))
        adesctxt = wx.StaticText(abottmpnl, -1, "Description:")
        self.accdscctrl = wx.TextCtrl(abottmpnl, -1, size=(200, -1), style= wx.TE_MULTILINE)
        self.accdlg.Bind(wx.EVT_BUTTON, self.OnSave, id=asavebtn.GetId())
        self.accdlg.Bind(wx.EVT_BUTTON, self.OnCancel, id=acancelbtn.GetId())
        ahtopsizer = wx.BoxSizer(wx.HORIZONTAL)

        ahbottomsizer = wx.BoxSizer(wx.VERTICAL)
        ahbottomsizer1 = wx.BoxSizer(wx.VERTICAL)

        ahtopsizer.Add(asavebtn, 0, wx.EXPAND | wx.ALL, 5)
        ahtopsizer.Add(acancelbtn, 0 , wx.EXPAND| wx.ALL, 5)


        atoppnl.SetSizer(ahtopsizer)
        ahbottomsizer.Add(ametertxt, 0, wx.ALL, 5)
        ahbottomsizer1.Add(adesctxt, 0, wx.ALL, 5)
        ahbottomsizer.Add(self.accctrl, 0, wx.ALL, 5)
        ahbottomsizer1.Add(self.accdscctrl, 0, wx.ALL, 5)

        abelowpsz = wx.BoxSizer(wx.HORIZONTAL)
        abelowpsz.Add(ahbottomsizer, 0, wx.EXPAND | wx.ALL, 5)
        abelowpsz.Add(ahbottomsizer1, 0, wx.EXPAND | wx.ALL, 5)
        abottmpnl.SetSizer(abelowpsz)
        if self.accstatus == 'Editing':
            newids = self.GetLocation()
            newids.addCallback(self.SetData)

        avsizer = wx.BoxSizer(wx.VERTICAL)
        avsizer.Add(atoppnl, 0, wx.EXPAND)
        avsizer.Add(abottmpnl, 1, wx.EXPAND)
        self.accdlg.SetSizer(avsizer)

        self.accdlg.ShowModal()
        self.accdlg.Destroy()
    def GetAccount(self):
        return self.QueryDb("""select account_no, Description from accounts where acc_id='%s'"""%(self.accposname))
    def SetData(self, result):
        for acc, desc in result:
            self.accctrl.SetValue(str(acc))
            if str(desc) != 'None':
                self.accdscctrl.SetValue(str(desc))
    def UpdateLocation(self):
        if self.accctrl.GetValue() == None or self.accctrl.GetValue() == '' or self.accctrl.GetValue() == 'None':
            wx.MessageBox(' Warning, fields cannot be empty', ' Warning', wx.ICON_WARNING)
        else:
            return self.QueryDb(""" update accounts set account_no ='%s', Description='%s' where acc_id = '%s'"""%(str(self.accctrl.GetValue()), str(self.accdscctrl.GetValue()), str(self.accposname)))
    def InsertLocation(self):
        if self.accctrl.GetValue() == None or self.accctrl.GetValue() == '' or self.accctrl.GetValue() == 'None':
            wx.MessageBox(' Warning, fields cannot be empty', ' Warning', wx.ICON_WARNING)
        else:
            return self.QueryDb("""insert into accounts (account_no, Description) values ('%s', '%s')"""%(str(self.accctrl.GetValue()), str(self.accdscctrl.GetValue())))
    def OnSave(self, event):
        if self.accstatus == 'Editing':
            update = self.UpdateLocation()
            update.addCallback(self.OnSuccess)
            update.addErrback(self.OnErr)
        else:
            insert = self.InsertLocation()
            insert.addCallback(self.OnSuccess)
            insert.addErrback(self.OnErr)
    def QueryDb(self, query):
        return self.accdbconn.runQuery(query)
    def OnSuccess(self, result):
        wx.MessageBox('Operation Successful', ' Operation info', wx.ICON_INFORMATION)
        self.accdlg.Destroy()
    def OnErr(self, err):
        wx.MessageBox('Operation Failed '+ str(err), ' Operation info', wx.ICON_ERROR)
    def OnCancel(self, event):
        self.accdlg.Destroy()
class Customers:
    def __init__(self, cdbconn, cposname, cstatus):
        #group e.g yamogo, order number
        self.cdbconn = cdbconn
        self.cposname = cposname
        self.cstatus = cstatus
    def SetData(self):
        pass
    def QueryDb(self, result):
        self.cdbconn.runQuery(result)
    def InsertCustomers(self):
        pass
    def UpdateCustomers(self):
        pass
if __name__ == "__main__":
    app=wx.App()
    app.MainLoop()