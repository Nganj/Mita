#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Starlord
#
# Created:     20/10/2015
# Copyright:   (c) Starlord 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import wx
import os
import shutil
import sys
import MySQLdb
import others
import wx.lib.agw.balloontip as btip
import wx.lib.imagebrowser as imagebrowser
class NewClient(wx.Frame):
    def __init__(self, parent, id, table, mode, status, mainconn):
        wx.Frame.__init__(self, parent, id, 'Edit ' + table, size=(1200, 600), style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
        self.status = status
        self.table = table
        self.mainconn = mainconn
        path = os.path.abspath("./Imagesm/meter.png")
        icon = wx.Icon(path, wx.BITMAP_TYPE_PNG)
        self.editid = mode
        self.SetIcon(icon)
        parentPanel = wx.Panel(self, -1, size= (-1,-1))
        vsizer = wx.BoxSizer(wx.VERTICAL)
        newtopPanel  = wx.Panel(parentPanel, -1, size=(-1, 60))
        newtopPanel.SetBackgroundColour('green')
        saveButton = wx.Button(newtopPanel, -1, "Save", (50, 20))
        cancelButton = wx.Button(newtopPanel, -1, "Cancel", (50, 20))
        self.lastpath = None
        dlg = imagebrowser.ImageDialog(self, self.lastpath)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=cancelButton.GetId())
        htopsizer = wx.BoxSizer(wx.HORIZONTAL)
        htopsizer.Add(saveButton, 0, wx.EXPAND | wx.ALL, 5)
        htopsizer.Add(cancelButton, 0, wx.EXPAND | wx.ALL, 5)
        newtopPanel.SetSizer(htopsizer)
##        self.newbottomPanel = wx.Panel(parentPanel, -1, size = (-1,-1))
        vsizer.Add(newtopPanel, 0, wx.EXPAND)
        if self.table == "Customers":
            self.cus = customerLayout(parentPanel, self.editid, self.status,dlg, self.mainconn)
            self.Bind(wx.EVT_BUTTON, self.cus.OnSave, id = saveButton.GetId())
            vsizer.Add(self.cus.nb, 1, wx.EXPAND)
        elif self.table == "Employees":
            self.emp = employeeLayout(parentPanel, self.editid, self.status,dlg, self.mainconn)
            self.Bind(wx.EVT_BUTTON, self.emp.OnSave, id = saveButton.GetId())
            vsizer.Add(self.emp.empnb, 1, wx.EXPAND)
        else:
            print "Invalid table"
##        self.newbottomPanel.SetSizer(self.cus.gridsz)



##        vsizer.Add(self.newbottomPanel, 1, wx.EXPAND | wx.ALL, 5)
        parentPanel.SetSizer(vsizer)
        self.Show()
##    def BrowsePhoto(self, event):

##        self.img = wx.Image("./Images/pic.jpg", type=wx.BITMAP_TYPE_ANY, index=-1)
##        self.sb1 = wx.StaticBitmap(self.imgpanel, -1, wx.BitmapFromImage(self.img))
##        if dlg.ShowModal() == wx.ID_OK:
##                # Save the last used path
##                self.lastpath = dlg.GetDirectory()
##                print self.lastpath
##                imgpath = dlg.GetFile()
    def scaleImg():
        pass
    def OnCancel(self, event):
        self.Destroy()
    def OnCloseWindow(self, event):
        self.Destroy()
##edit and insert layout for employees
class employeeLayout:
    def __init__(self, epanel, empid, status, dlg, conn):
        self.epanel = epanel
        self.dlg = dlg
        self.empid = empid
        self.status = status
        self.mainconn = conn
        self.empnb = wx.Notebook(self.epanel)
        self.emppanel = wx.Panel(self.empnb)
        self.emplastpath = None
        self.empimgpath = None
        self.finalimgpath = None

        self.setcombolists = None

        self.emppanel1 = wx.Panel(self.empnb)


        self.empnb.AddPage(self.emppanel, "Employee settings    ")
        self.empnb.AddPage(self.emppanel1, "User login   ")


        self.empGrid = wx.GridBagSizer(vgap=8, hgap=8)
        self.imgEmpPanel = wx.Panel(self.emppanel, size=(200, 300), style=wx.BORDER_SUNKEN)

        self.fenametxt = wx.StaticText(self.emppanel, -1, "First Name")
        self.fenamectrl =wx.TextCtrl(self.emppanel, -1, size=(200, -1))
        self.senametxt = wx.StaticText(self.emppanel, -1, "Second Name")
        self.senamectrl =wx.TextCtrl(self.emppanel, -1, size=(200, -1))
        self.lenametxt = wx.StaticText(self.emppanel, -1, "Last Name")
        self.lenamectrl = wx.TextCtrl(self.emppanel, -1, size=(200, -1))
        self.usernametxt = wx.StaticText(self.emppanel, -1, "Login Username")

        self.national_name = wx.StaticText(self.emppanel, -1, "National Id")
        self.national_id = wx.TextCtrl(self.emppanel, -1, size=(200, -1))


        self.userlist = []
        self.usercombo = self.GetComboData('username', 'credentials')
        self.usercombo.addCallback(self.PopulateUsers)

        self.usernamectrl = wx.ComboBox(self.emppanel, -1, size=(200, -1), choices=[], style= wx.CB_READONLY)
        self.adduser = wx.Button(self.emppanel, -1, ' + ')
        self.emppanel.Bind(wx.EVT_BUTTON, others.Agents(self.mainconn, 'None', 'Inserting').DisplayAgents, id=self.adduser.GetId())
        self.assignloctxt = wx.StaticText(self.emppanel, -1, ("Assigned\nArea"))
        self.locationlist = []

        self.usercombo = self.GetComboData('location', 'location')
        self.usercombo.addCallback(self.PopulateLocation)
        self.assignlocctrl = wx.ComboBox(self.emppanel, -1, size=(200, -1), choices = [], style= wx.CB_READONLY)
        self.addlocation = wx.Button(self.emppanel,  -1, ' + ')
        self.emppanel.Bind(wx.EVT_BUTTON, others.Location(self.mainconn, 'None', 'Inserting').DisplayLocation, id=self.addlocation.GetId())

        self.eemailtxt = wx.StaticText(self.emppanel, -1, "Email")
        self.eemailctrl = wx.TextCtrl(self.emppanel, -1, size=(200, -1))
        self.ephonetxt = wx.StaticText(self.emppanel, -1, "Phone")
        self.ephonectrl = wx.TextCtrl(self.emppanel, -1, size=(200, -1))
        self.homelocationtxt = wx.StaticText(self.emppanel, -1, "Home \nAddress")
        self.homelocationctrl = wx.TextCtrl(self.emppanel, -1, size=(200, -1), style = wx.TE_MULTILINE)
        self.position = wx.StaticText(self.emppanel, -1, "Position")
        self.positionlist = []
        self.usercombo = self.GetComboData('position', 'position')
        self.usercombo.addCallback(self.PopulatePosition)
        self.positionctrl = wx.ComboBox(self.emppanel, -1,  size=(200, -1), choices =[], style= wx.CB_READONLY)
        self.addposition = wx.Button(self.emppanel, -1, ' + ')
        self.emppanel.Bind(wx.EVT_BUTTON, others.Position(self.mainconn, 'None', 'Inserting').Displaydlg, id=self.addposition.GetId())
        self.empBrowse = wx.Button(self.emppanel, -1, 'Browse Image.... ')
        self.emppanel.Bind(wx.EVT_BUTTON, self.BrowseEmpPhoto, id=self.empBrowse.GetId())

        self.empGrid.Add(self.imgEmpPanel, (1,1), (6, 3))
        self.empGrid.Add(self.fenametxt, (1, 4), (1, 3))
        self.empGrid.Add(self.fenamectrl, (1, 8) , (1, 3))
        self.empGrid.Add(self.senametxt, (1, 13), (1, 3))
        self.empGrid.Add(self.senamectrl, (1, 17), (1, 3))

        self.empGrid.Add(self.lenametxt, (2, 4), (1, 3))
        self.empGrid.Add(self.lenamectrl, (2, 8), (1, 3))
        self.empGrid.Add(self.ephonetxt, (2, 13), (1, 3))
        self.empGrid.Add(self.ephonectrl, (2, 17), (1, 3))

        self.empGrid.Add(self.usernametxt, (3, 4),(1, 3))
        self.empGrid.Add(self.usernamectrl, (3, 8), (1, 3))
        self.empGrid.Add(self.adduser, (3, 12), (1, 1))
        self.empGrid.Add(self.national_name, (3, 13), (1, 3))
        self.empGrid.Add(self.national_id, (3, 17), (1, 3))

        self.empGrid.Add(self.assignloctxt, (4, 4), (1, 3))
        self.empGrid.Add(self.assignlocctrl, (4, 8), (1, 3))
        self.empGrid.Add(self.addlocation, (4, 12),(1,1))

        self.empGrid.Add(self.eemailtxt, (4, 13), (1, 3))
        self.empGrid.Add(self.eemailctrl, (4, 17), (1, 3))

        self.empGrid.Add(self.homelocationtxt, (5, 4), (1, 3))
        self.empGrid.Add(self.homelocationctrl, (5, 8), (2, 3))
        self.empGrid.Add(self.position, (5, 13), (1, 3))
        self.empGrid.Add(self.positionctrl,(5, 17), (1, 3))
        self.empGrid.Add(self.addposition, (5, 20), (1,1))

        self.empGrid.Add(self.empBrowse, (7, 1), (1, 3))
        self.emppanel.SetSizer(self.empGrid)

        self.gesizer = wx.GridBagSizer(vgap=8, hgap=8)
        self.usertxt = wx.StaticText(self.emppanel1, -1, "Username")
        self.userctrl = wx.TextCtrl(self.emppanel1, -1 , size=(200, -1))
        self.userctrl.Disable()
        self.paswdtxt = wx.StaticText(self.emppanel1, -1, "Password")
        self.passwdctrl = wx.TextCtrl(self.emppanel1, -1, size=(200, -1), style=wx.TE_PASSWORD)
        self.passwdctrl.Disable()
        self.passwd2txt = wx.StaticText(self.emppanel1, -1, "Confirm Password")
        self.passwd2ctrl = wx.TextCtrl(self.emppanel1, -1, size=(200, -1), style = wx.TE_PASSWORD)
        self.passwd2ctrl.Disable()

        self.gesizer.Add(self.usertxt, (1, 1), (1, 3))
        self.gesizer.Add(self.userctrl, (1, 4), (1, 3))
        self.gesizer.Add(self.paswdtxt, (2, 1), (1, 3))
        self.gesizer.Add(self.passwdctrl, (2,4), (1, 3))
        self.gesizer.Add(self.passwd2txt, (3, 1), (1, 3))
        self.gesizer.Add(self.passwd2ctrl, (3, 4), (1, 3))
        self.emppanel1.SetSizer(self.gesizer)
        if self.status == 'Edit':
            self.e = self.getEmployee()
            self.e.addCallback(self.editEmployee)
            self.emppanel1.Refresh()
        else:
            pass
##            self.delEmployee(self.status)
        self.empcols = ['f_name', 's_name', 'l_name', 'credentials_user_id', 'location_location_id', 'email', 'phone_no', 'physical_address', 'position_off', 'empl_image']
        self.empctrl =['self.fenamectrl','self.senamectrl','self.lenamectrl','self.usernamectrl','self.assignlocctrl','self.eemailctrl','self.ephonectrl','self.homelocationctrl',  'self.positionctrl','self.empimgpath']
        '''a.f_name, a.s_name, a.l_name, c.username, b.locationlocation, a.email, a.phone_no, a.physical_address, d.position, a.empl_image'''
    def PopulateUsers(self, result):
        for data in result:
            for item in data:
                    self.userlist.append(item)
        self.usernamectrl.SetItems(self.userlist)
    def PopulatePosition(self, result):
        for data in result:
            for item in data:
                    self.positionlist.append(item)
        self.positionctrl.SetItems(self.positionlist)
    def PopulateLocation(self, result):
        for data in result:
            for item in data:
                    self.locationlist.append(item)
        self.assignlocctrl.SetItems(self.locationlist)
    def GetComboData(self, tblcol, dbtable):
        self.tblcol = tblcol
        self.dbtable = dbtable
        query = 'select '+self.tblcol+' from ' + self.dbtable
        return self.mainconn.runQuery(query)
    def OnClickUser(self, event):
        pass
    def OnClickLocation(self, event):
        pass
    def BrowseEmpPhoto(self, event):
        if self.dlg.ShowModal() == wx.ID_OK:
                def copyFile(src, dest):
                    try:
                        shutil.copy(src, dest)
                        # eg. src and dest are the same file
                    except shutil.Error as e:
                            wx.MessageBox('Error: %s' % e, 'Error', style=wx.ICON_ERROR)
                      # eg. source or destination doesn't exist
                    except IOError as e:
                        wx.MessageBox('Error: %s' % e.strerror, 'Error', style=wx.ICON_ERROR)
                # Save the last used path
                self.emplastpath = self.dlg.GetDirectory()
                self.empimgpath = self.dlg.GetFile()
                img =  self.empimgpath.split('\\')[-1]
                imgtypes = ['png','bmp','jpg','jpeg','tiff']
                #confirm image type
                if img.split('.')[-1] in imgtypes and 'employees':
                    #check if image exists in folder
                    if os.path.isfile(os.getcwd()+'\\\\Imagesm\\employees\\\\emp'+str(self.empid)+'.'+img.split('.')[-1]):
                        edlg = wx.MessageDialog(None, 'Another employee file exists, do you want to delete it?', 'File Exists dialog', style=wx.YES_NO|wx.ICON_QUESTION)
                        listen_edlg = edlg.ShowModal()
                        if listen_edlg == wx.ID_YES:
                            os.remove(os.getcwd()+'\\Imagesm\\employees\\emp'+str(self.empid)+'.'+img.split('.')[-1])
                            copyFile(self.empimgpath, os.getcwd()+'\\\\Imagesm\\\\employees')
                            os.rename(os.getcwd()+'\\\\Imagesm\\\\employees\\\\'+img, os.getcwd()+'\\\\Imagesm\\employees\\\\emp'+str(self.empid)+'.'+img.split('.')[-1])
                            self.finalimgpath = os.getcwd().replace('\\','\\\\')+'\\\\Imagesm\\\\employees\\\\emp'+str(self.empid)+'.'+img.split('.')[-1]

                        else:
                            pass
                        edlg.Destroy()
                    else:
                        copyFile(self.empimgpath, os.getcwd()+'\\Imagesm\\employees')
                        os.rename(os.getcwd()+'\\Imagesm\\employees\\'+img, os.getcwd()+'\\Imagesm\\employees\\emp'+str(self.empid)+'.'+img.split('.')[-1])
                        self.finalimgpath = os.getcwd().replace('\\','\\\\')+'\\\\Imagesm\\\\employees\\\\emp'+str(self.empid)+'.'+img.split('.')[-1]

                else:
                    wx.MessageBox('Invalid image type', 'File error', style=wx.STAY_ON_TOP|wx.ICON_WARNING)
                try:
                    self.empimg = wx.Image(self.empimgpath, type=wx.BITMAP_TYPE_ANY, index=-1)
                    self.scaledImg = self.empimg.Scale(200, 300)
                    self.sb1 = wx.StaticBitmap(self.imgEmpPanel, -1, wx.BitmapFromImage(self.scaledImg))
                    self.imgEmpPanel.Refresh()
                except Exception:
                    wx.MessageBox('Profile image cannot be found', 'Image Error', wx.ICON_ERROR)
    def editEmployee(self, result):
        i = 0
        for rows in result:
            for col in range(0, len(self.empctrl)):
                if self.empctrl[i] != 'self.empimgpath':
                    txtctrl = eval(self.empctrl[i])
                    #populate combo boxes
                    if self.empctrl[i] == 'self.usernamectrl' or self.empctrl[i] == 'self.assignlocctrl' or self.empctrl[i] == 'self.positionctrl':
                        # check none types and update approriately
                        if rows[i+1] != None:
                            txtctrl.SetValue(rows[i+1])
                        else:
##                            txtctrl.SetValue('')
                             pass
                    else:
                        if rows[i+1] != None:
                            txtctrl.AppendText(rows[i+1])
                        else:
                            pass
##                            txtctrl.AppendText('')
                elif self.empctrl[i] == 'self.empimgpath':
                    if rows[i+1] != 'None' and rows[i+1] != None and rows[i+1] != '':
                        self.finalimgpath = rows[i+1].replace('\\','\\\\')
                        self.empimg = wx.Image(rows[i+1], type=wx.BITMAP_TYPE_ANY, index=-1)
                        self.scaledImg = self.empimg.Scale(200, 300)
                        self.sb1 = wx.StaticBitmap(self.imgEmpPanel, -1, wx.BitmapFromImage(self.scaledImg))
                        self.imgEmpPanel.Refresh()
                    else:
                        pass
                else:
                    pass
                i += 1
    def delEmployee(self, text):
        print text + ' employee'
    def getEmployee(self):
        return self.mainconn.runQuery('select  a.emp_id, a.f_name, a.s_name, a.l_name, c.username, b.location, a.email, a.phone_no, a.physical_address, d.position, a.empl_image  from employees a left join location b on b.location_id = a.location_location_id left join credentials c on a.credentials_user_id = c.user_id left join position d on a.position_off = d.position_id where a.emp_id = %s', (self.empid))
        ##edit and insert layout for customer
    def OnSave(self, event):
        for txtctrl in range(0, len(self.empctrl)):
            col = eval(self.empctrl[txtctrl])

            if self.empctrl[txtctrl] == 'self.usernamectrl' or self.empctrl[txtctrl] == 'self.assignlocctrl' or self.empctrl[txtctrl]== 'self.positionctrl':
                data = col.GetStringSelection()
                if self.empctrl[txtctrl] == 'self.usernamectrl':
                        query = """Update employees set %s = (select user_id from credentials where username = "%s") where emp_id = %s;"""%(self.empcols[txtctrl], data, str(self.empid))
                        self.q = self.OnUpdate(query)
                        self.q.addErrback(self.OnErr)
                elif self.empctrl[txtctrl] == 'self.assignlocctrl':
                        query = """update employees set %s = (select location_id from location where location = "%s") where emp_id = %s;"""%(self.empcols[txtctrl], data, str(self.empid))
                        self.q = self.OnUpdate(query)
                        self.q.addErrback(self.OnErr)
                elif self.empctrl[txtctrl] == 'self.positionctrl':
                        query = """Update employees set %s = (select position_id from position where position = "%s") where emp_id = %s;"""%(self.empcols[txtctrl], data, str(self.empid))
                        self.q = self.OnUpdate(query)
                        self.q.addErrback(self.OnErr)
            elif self.empctrl[txtctrl] == 'self.empimgpath':
                query = """Update employees set %s = '%s' where emp_id = %s;"""%(self.empcols[txtctrl], self.finalimgpath, str(self.empid))
                self.q = self.OnUpdate(query)
                self.q.addErrback(self.OnErr)

            else:
                try:
                    data = col.GetValue()
                    query = """Update Employees set %s = '%s' where emp_id = %s;"""%(self.empcols[txtctrl], data, self.empid)
                    self.q = self.OnUpdate(query)
                    self.q.addErrback(self.OnErr)
                except Exception:
                    wx.MessageBox(str(Exception), 'Warning Box', style=wx.ICON_WARNING|wx.STAY_ON_TOP)
    def OnUpdate(self, query):
        return self.mainconn.runOperation(query)
    def OnErr(self, result):
        wx.MessageBox("Check that username is not in use or the information entered is in the correct format", '   Warning Box', style=wx.ICON_WARNING|wx.STAY_ON_TOP)
class customerLayout:
    def __init__(self, cpanel, cid, cstatus, cdlg, cconn):
        self.cid = cid
        self.cpanel = cpanel
        self.cdlg = cdlg
        self.cconn = cconn
        self.cstatus= cstatus
        self.nb = wx.Notebook(self.cpanel)
        self.panel1 = wx.Panel(self.nb)

        self.panel2 = wx.Panel(self.nb)


        self.nb.AddPage(self.panel1, "Main    ")
        self.nb.AddPage(self.panel2, "Other     ")
        self.lastpath = None

        self.gridsz = wx.GridBagSizer(vgap=8, hgap=8)
        self.imgpanel =wx.Panel(self.panel1, size=(150,150), style=wx.BORDER_SUNKEN)


        fname = wx.StaticText(self.panel1, -1, 'First Name')
        self.fnameTxtCtrl = wx.TextCtrl(self.panel1, -1, size=(200, -1))

        groupname = wx.StaticText(self.panel1, -1, 'Group Name')
        groupctrl = wx.ComboBox(self.panel1, -1, choices=['None', 'Yamogo','Waguthu','Ndenderu','Dadgu'], style=wx.CB_READONLY)

        national_id = wx.TextCtrl(self.panel1, -1, size=(200, -1))
        national_name = wx.StaticText(self.panel1, -1, "National Id")

        sname = wx.StaticText(self.panel1, -1, 'Second Name')
        snameTxtCtrl = wx.TextCtrl(self.panel1, -1, size=(200, -1))
        lname = wx.StaticText(self.panel1, -1, 'Last Name')
        lnameTxtCtrl = wx.TextCtrl(self.panel1, -1, size=(200, -1))
        phone = wx.StaticText(self.panel1, -1, 'Phone')
        phoneTxtCtrl = wx.TextCtrl(self.panel1, -1, size=(200, -1))
        brwsebtn = wx.Button(self.panel1, -1, 'Browse Photo...')
        self.panel1.Bind(wx.EVT_BUTTON, self.BrowsePhoto, id=brwsebtn.GetId())
        email = wx.StaticText(self.panel1, -1, 'Email')
        emailTxtCtrl = wx.TextCtrl(self.panel1, -1, size=(350, -1))
        account = wx.StaticText(self.panel1, -1, 'Account Number')
        accountTxtCtrl = wx.ComboBox(self.panel1, -1, size=(350, -1), choices=['mita0001','mita0002','mita0003'], style=wx.CB_READONLY)
        addaccount = wx.Button(self.panel1, -1, '  +  ', size=(35,-1))
        defaultcheck = wx.CheckBox(self.panel1, -1, 'Use Default Naming')
        meter = wx.StaticText(self.panel1, -1, 'Meter Number')
        meterTxtCtrl = wx.TextCtrl(self.panel1, -1, size=(350, -1))
        sublocation = wx.StaticText(self.panel1, -1, 'Locality')
        locality = wx.Button(self.panel1, -1, '  +  ', size=(35,-1))
        self.panel1.Bind(wx.EVT_BUTTON, self.choiceLocality, id=locality.GetId())
        subloc = ["Thimbigua", "Karura", "Kiongora", "Kiambaa"]
        self.sublocationCombo = wx.ComboBox(self.panel1, -1, size=(350, -1), choices=subloc, style=wx.CB_READONLY)
        desc = wx.StaticText(self.panel1, -1, 'Description')
        descTxtCtrl = wx.TextCtrl(self.panel1, -1, size=(350, 100), style=wx.TE_MULTILINE)
        self.gridsz.Add(self.imgpanel, (1,1), (5,3))
        self.gridsz.Add(fname, (1, 4))
        self.gridsz.Add(self.fnameTxtCtrl, (1, 5), (1,3))
        self.gridsz.Add(national_name, (3, 9))
        self.gridsz.Add(national_id, (3, 10), (1,3))
        self.gridsz.Add(groupname, (4, 9))
        self.gridsz.Add(groupctrl, (4, 10), (1,3))
        self.gridsz.Add(sname, (2, 4))
        self.gridsz.Add(snameTxtCtrl, (2, 5), (1,3))
        self.gridsz.Add(lname, (3, 4))
        self.gridsz.Add(lnameTxtCtrl, (3, 5), (1,3))
        self.gridsz.Add(phone, (4, 4))
        self.gridsz.Add(phoneTxtCtrl, (4, 5), (1,3))
        self.gridsz.Add(brwsebtn, (5, 4), (1, 3))
        self.gridsz.Add(email, (6, 1))
        self.gridsz.Add(emailTxtCtrl, (6, 2), (1,5))
        self.gridsz.Add(account, (7 ,1))
        self.gridsz.Add(accountTxtCtrl, (7, 2), (1,5))
        self.gridsz.Add(addaccount, (7, 8), (1,1))
        self.gridsz.Add(defaultcheck, (7, 10), (1, 3))
        self.gridsz.Add(meter, (8, 1))
        self.gridsz.Add(meterTxtCtrl, (8, 2), (1,5))
        self.gridsz.Add(sublocation, (9, 1))
        self.gridsz.Add(self.sublocationCombo, (9, 2), (1,5))
        self.gridsz.Add(locality, (9, 8), (1,1))
        self.gridsz.Add(desc, (10, 1))
        self.gridsz.Add(descTxtCtrl, (10, 2), (6,5))
##        sizer.Add(self.nb, 1, wx.EXPAND)
        self.panel1.SetSizer(self.gridsz)

##call edit method when mode has something
##        if self.cusmode is not 0:
##            self.editcusinterface()
        self.cdlg.Destroy()
    def editcusinterface(self):
        self.fnameTxtCtrl.AppendText('James')
    def choiceLocality(self, event):
        choices = ["Thimbigua", "Karura", "Kiongora", "Kiambaa"]
        dialog = wx.SingleChoiceDialog(None, "Pick locality", "Sublocations", choices)
        if dialog.ShowModal() == wx.ID_OK:
            print "You selected: %s\n" % dialog.GetStringSelection()
            self.sublocationTxtCtrl.AppendText(dialog.GetStringSelection())
        dialog.Destroy()
##edit and insert layout for location
    def BrowsePhoto(self, event):
        if self.dlg.ShowModal() == wx.ID_OK:
                # Save the last used path

                self.lastpath = self.dlg.GetDirectory()

                imgpath = self.dlg.GetFile()
                self.img = wx.Image(imgpath, type=wx.BITMAP_TYPE_ANY, index=-1)
                self.sb1 = wx.StaticBitmap(self.imgpanel, -1, wx.BitmapFromImage(self.img))
                self.panel1.Refresh()
##                bitmap = wx.Bitmap(imgpath)

##                if bitmap.IsOk():
##                    self.bmp.SetBitmap(bitmap)
##                    self.Layout()
##                    self.bmp.Refresh()
        self.dlg.Destroy()
    def OnSave(self, event):
        pass
class locationLayout:
    pass
if __name__ == '__main__':
    app = wx.App()
    app.MainLoop()
