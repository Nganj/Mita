#!/usr/bin/env python
import wx
import wx.lib.mixins.listctrl  as  listmix
import sys
##del sys.modules['twisted.internet.reactor']
from twisted.internet import wxreactor
wxreactor.install()
import time
import os
##import clients
import secondary
import others
import Main
import dbreg
from zope.interface import implements, Interface
from twisted.cred import checkers, credentials, portal
from twisted.internet import protocol, reactor
from twisted.protocols import basic
import hashlib
def hash(password):
    return hashlib.md5(password).hexdigest()
data = [('new', 'column', 'name'), ('hurray', 'dash', 'bellow')]
class AutoWidthListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent):
      wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
      listmix.ListCtrlAutoWidthMixin.__init__(self)
      #listmix.TextEditMixin.__init__(self)
class MainGui(wx.Frame, wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.ColumnSorterMixin):
    def __init__(self, parent, id):

        self.coname = 'Mita Water Application'
        wx.Frame.__init__(self, parent, id, self.coname)
        path = os.path.abspath("./Imagesm/meter.png")
        icon = wx.Icon(path, wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)
        self.panel = wx.Panel(self)
        self.panel.SetLabel('hello suckers, work bitch')
##        self.panel.SetBackgroundColour('blue')
        self.Maximize()
        wx.SYS_COLOUR_WINDOWFRAME
        #create menu bar
        menubar = wx.MenuBar()
        file = wx.Menu()
        reports = wx.Menu()
        chat = wx.Menu()
        options = wx.Menu()
        masters = wx.Menu()
        file.Append(1, 'Export', 'Export Records To Excel')
        file.Append(2, 'Import', 'Import Records From Excel/CSV file')
        file.Append(3, 'Backup')
        file.Append(4, 'Restore')
        file.Append(19, 'Quit', 'Quit Application')

        masters.Append(5, 'Company')
        masters.Append(6, 'Employees')
        masters.Append(7, 'Customers')
        masters.Append(8, 'Agents')
        masters.Append(9, 'Location')
        masters.Append(10, 'Sublocation')
        masters.Append(11, 'Accounts')
        masters.Append(20, 'Position')

        reports.Append(11, 'Customer History', 'Customer Consumption History')
        reports.Append(12, 'Location Consumption', ' Categorize Consumption Per Location')
        reports.Append(13, 'Overall Consumption', 'Total Consumption Of The Month')
        chat.Append(14, 'Send Broadcast', 'Broadcast To Everyone In The Field')
        chat.Append(15, 'Send to one agent', 'Message An Agent')
        options.Append(16, 'Preferences', 'System Settings')
        options.Append(17, 'About Us', 'About Mazecoders')
        options.Append(18, 'Help', 'Software Assistance')

        '''bind menu items'''
        self.Bind(wx.EVT_MENU, self.OnCloseWindow, id=4)
        self.Bind(wx.EVT_MENU, self.Company, id=5)
        self.Bind(wx.EVT_MENU, self.employees, id=6)
        self.Bind(wx.EVT_MENU, self.clientele, id=7)
        self.Bind(wx.EVT_MENU, self.Agents, id=8)
        self.Bind(wx.EVT_MENU, self.location, id=9)
        self.Bind(wx.EVT_MENU, self.sublocation, id=10)
        self.Bind(wx.EVT_MENU, self.accounts, id=11)
        self.Bind(wx.EVT_MENU, self.Position, id=20)


        menubar.Append(file, '&File')
        menubar.Append(masters, '&Masters')
        menubar.Append(reports, '&Reports')
        menubar.Append(chat, '&Chat')
        menubar.Append(options, '&Options')
        self.SetMenuBar(menubar)
        #create statusbar

        self.sb = self.CreateStatusBar()
        vsizer = wx.BoxSizer(wx.VERTICAL)
        htopsizer = wx.BoxSizer(wx.HORIZONTAL)
        toppanel = wx.Panel(self.panel, size = (-1, 50),style=wx.RAISED_BORDER)
        topdatesizer = wx.BoxSizer(wx.HORIZONTAL)
        panelexpand = wx.Panel(toppanel, size = (-1, 40), style=wx.ALIGN_LEFT)
        self.search = wx.SearchCtrl(toppanel, size=(120, -1), style=wx.TE_PROCESS_ENTER)
        dpc = wx.DatePickerCtrl(toppanel, size=(120,-1), style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY | wx.DP_ALLOWNONE | wx.ALIGN_RIGHT,  )
        dpctwo = wx.DatePickerCtrl(toppanel, size=(120,-1), style = wx.DP_DROPDOWN | wx.DP_SHOWCENTURY | wx.DP_ALLOWNONE | wx.ALIGN_RIGHT )
        sampleList =['Select category','Location', 'Sublocation', 'Customer']
        dropdown = wx.ComboBox(toppanel, -1, "select category", (120, -1), wx.DefaultSize, sampleList, wx.CB_DROPDOWN)
        topconsumers = wx.StaticText(toppanel, -1 , 'Top Consumers By:', (200, 45))
        stfrom = wx.StaticText(toppanel, -1 , 'From:', (200, 45))
        stto = wx.StaticText(toppanel, -1 , 'To:', (200, 45))
        viewbtn = wx.Button(toppanel, -1, 'View', (150, 50))
        font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        stfrom.SetFont(font)
        topdatesizer.Add(panelexpand, 1)
        stto.SetFont(font)
        topconsumers.SetFont(font)

        topdatesizer.Add(topconsumers, 0, wx.TOP | wx.RIGHT, 10)
        topdatesizer.Add(dropdown, 0, wx.TOP | wx.RIGHT, 10)
        topdatesizer.Add(self.search, 0, wx.TOP | wx.RIGHT, 10)
        topdatesizer.Add(stfrom, 0, wx.TOP| wx.RIGHT, 10)
        topdatesizer.Add(dpc, 0, wx.TOP | wx.RIGHT, 10)
        topdatesizer.Add(stto, 0, wx.TOP | wx.RIGHT, 10)
        topdatesizer.Add(dpctwo, 0, wx.TOP | wx.RIGHT, 10)
        topdatesizer.Add(viewbtn, 0, wx.TOP | wx.RIGHT, 10)

        toppanel.SetSizer(topdatesizer)

##style=wx.RAISED_BORDER
        toppanel.SetBackgroundColour('green')
        htopsizer.Add(toppanel, 1, wx.EXPAND)

        hmidsizer = wx.BoxSizer(wx.HORIZONTAL)
        midpanelone = wx.Panel(self.panel, size = (150, -1), style=wx.SUNKEN_BORDER)
        midpanelone.SetBackgroundColour('blue')
        bmp = wx.Image("reportIMG.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        bmpmaster = wx.Image("master.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        bmpsettings = wx.Image("settings.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        bmpchat = wx.Image("chat.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()

        self.button = wx.BitmapButton(midpanelone, -1, bmp, pos=(10, 20))
        self.btnmaster = wx.BitmapButton(midpanelone, -1, bmpmaster, pos=(10, 20))
        self.btnsettings = wx.BitmapButton(midpanelone, -1, bmpsettings, pos=(10, 20))
        self.btnchat = wx.BitmapButton(midpanelone, -1, bmpchat, pos=(10, 20))

##        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)
        self.button.SetDefault()
        midpanelonesizer = wx.BoxSizer(wx.VERTICAL)
        midpanelonesizer.Add(self.button, 0 , wx.ALL, 10)
        midpanelonesizer.Add(self.btnmaster, 0 , wx.ALL, 10)
        midpanelonesizer.Add(self.btnsettings, 0 , wx.ALL, 10)
        midpanelonesizer.Add(self.btnchat, 0 , wx.ALL, 10)
        midpanelone.SetSizer(midpanelonesizer)


        midpaneltwo = wx.Panel(self.panel, size = (-1, -1))
        midpaneltwo.SetBackgroundColour('gray')
        midpaneltwosizer = wx.BoxSizer(wx.VERTICAL)
##        midtoppanel = wx.Panel(midpaneltwo, size = (-1, 30), style=wx.RAISED_BORDER)
##        midtoppanel.SetBackgroundColour('white')
##        topconsumers = wx.StaticText(midtoppanel, -1 , 'Top Consumers by location', (200, 45))
##        insidemidtoppanel = wx.Panel(midtoppanel, size= (-1, 30))
##        topmidpanelsizer = wx.BoxSizer(wx.HORIZONTAL)
##        topmidpanelsizer.Add(topconsumers, 0, wx.ALL | wx.EXPAND, 5)
##        topmidpanelsizer.Add(insidemidtoppanel, 1)
##        midtoppanel.SetSizer(topmidpanelsizer)


        midmidpanel = wx.Panel(midpaneltwo, size = (-1, -1), style=wx.RAISED_BORDER)
        midmidpanel.SetBackgroundColour('Gray')
        midbelowpanel = wx.Panel(midpaneltwo, size = (-1, 250), style=wx.RAISED_BORDER)
##        midpaneltwosizer.Add(midtoppanel, 0, wx.ALL, 5)
        midpaneltwosizer.Add(midmidpanel, 1,  wx.EXPAND | wx.ALL , 5)
        midpaneltwosizer.Add(midbelowpanel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)
        midpaneltwo.SetSizer(midpaneltwosizer)


##        wx.StaticText(midpaneltwo, -1, "Water is life")
        midpanelthree = wx.Panel(self.panel, size = (150,-1), style=wx.SUNKEN_BORDER)
        midpanelthree.SetBackgroundColour('blue')
        hmidsizer.Add(midpanelone, 0,  wx.EXPAND)
        hmidsizer.Add(midpaneltwo, 1, wx.EXPAND)
        hmidsizer.Add(midpanelthree, 0, wx.EXPAND)
        panelthreevsizer = wx.BoxSizer(wx.VERTICAL)
##set previous and next and refrsh buttons
        btnprev = wx.Button(midpanelthree, -1, 'Previous', size = (65, 30))
        btnnext = wx.Button(midpanelthree, -1, 'Next', size = (65, 30))

        btnrefresh = wx.Button(midpanelthree, -1, 'Refresh', size = (65, 30))
        btnonff = wx.Button(midpanelthree, -1, 'Turn chat on/off', size = (100, 30))
        togglechatsizer = wx.BoxSizer(wx.HORIZONTAL)
        togglechatsizer.Add(btnrefresh, 0, wx.ALL, 5)
        togglechatsizer.Add(btnonff, 0, wx.ALL, 5)

        multiText = wx.TextCtrl(midpanelthree, -1,
        "Chat and Broadcast server", size=(200, 300), style=wx.TE_MULTILINE | wx.TE_READONLY)
        multiText.SetInsertionPoint(0)
        chatsizer = wx.BoxSizer(wx.HORIZONTAL)
        chatbox = wx.TextCtrl(midpanelthree, -1, size=(130, 40), style=wx.TE_WORDWRAP)
        sendbtn = wx.Button(midpanelthree, -1, 'Send', size = (50, 40))
        chatsizer.Add(chatbox, 0, wx.ALL, 5)
        chatsizer.Add(sendbtn, 0, wx.ALL, 5)

        midlastpanel = wx.Panel(midpanelthree, size =(150, -1))
        panelthreevsizer.Add(btnprev, 0, wx.ALL, 10)
        panelthreevsizer.Add(btnnext, 0, wx.ALL, 10)
        panelthreevsizer.Add(togglechatsizer, 0, wx.ALL, 10)
        panelthreevsizer.Add(multiText, 0, wx.ALL, 10)
        panelthreevsizer.Add(chatsizer, 0, wx.ALL, 10)
        panelthreevsizer.Add(midlastpanel, 1)
        midpanelthree.SetSizer(panelthreevsizer)

        vsizer.Add(htopsizer, 0, wx.EXPAND)
        vsizer.Add(hmidsizer, 1, wx.EXPAND)

        self.panel.SetSizer(vsizer)
        vsizer.Fit(self)
        #initialize virtual list parameters
        self.list = AutoWidthListCtrl(midmidpanel)

        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        str(data)

        self.list.InsertColumn(0, 'Number', width=70)
        self.list.InsertColumn(1, 'Name', width=140)
        self.list.InsertColumn(2, 'Date', width=130)
        self.list.InsertColumn(3, 'Price', width=140)
        self.list.InsertColumn(4, 'Quantity in Kgs', width=140)
        self.list.InsertColumn(5, 'Description', wx.LIST_FORMAT_RIGHT, 140)
        flag = 1
        for i in data:
            index = self.list.InsertStringItem(sys.maxint, str(flag))
            self.list.SetStringItem(index, 1, i[0])
            self.list.SetStringItem(index, 2, i[1])
            self.list.SetStringItem(index, 3, i[2])
##            self.list.SetStringItem(index, 4, i[3])
##            self.list.SetStringItem(index, 5, i[4])
            flag += 1

##        listpanel = wx.Panel(midmidpanel, size = (200, -1))

        self.hbox1.Add(self.list,  1, wx.EXPAND)
##        self.hbox1.Add(listpanel, 0, wx.EXPAND | wx.ALIGN_RIGHT)
        midmidpanel.SetSizer(self.hbox1)
        midmidpanel.Layout()
        #self.splitter.UpdateSize()

        # end virtual list parameters
        # Initialise the below  middle panel
        iconsz = wx.GridBagSizer(vgap=2, hgap=2)
        clientbmp = wx.Image("cus.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.client_bmp = wx.BitmapButton(midbelowpanel, -1, clientbmp, pos=(10, 20))
        self.Bind(wx.EVT_BUTTON, self.clientele, id=self.client_bmp.GetId())
        clientctrl = wx.StaticText(midbelowpanel, -1, 'Customers')

        empbmp = wx.Image("empo.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.emp_bmp = wx.BitmapButton(midbelowpanel, -1, empbmp, pos=(10, 20))
        self.Bind(wx.EVT_BUTTON, self.employees, id=self.emp_bmp.GetId())
        empctrl = wx.StaticText(midbelowpanel, -1, 'Employees')

        placesbmp = wx.Image("place.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.places_bmp = wx.BitmapButton(midbelowpanel, -1, placesbmp, pos=(10, 20))
        self.Bind(wx.EVT_BUTTON, self.location, id=self.places_bmp.GetId())
        placesctrl = wx.StaticText(midbelowpanel, -1, 'Locations')

        chatbmp = wx.Image("chatnew.bmp", wx.BITMAP_TYPE_BMP).ConvertToBitmap()
        self.chat_bmp = wx.BitmapButton(midbelowpanel, -1, chatbmp, pos=(10, 20))
        chatctrl = wx.StaticText(midbelowpanel, -1, 'Chats')

        iconsz.Add(self.client_bmp, (1,1))
        iconsz.Add(clientctrl, (2, 1))
        iconsz.Add(self.emp_bmp, (1,2), (1, 1))
        iconsz.Add(empctrl, (2, 2), (1,1))
        iconsz.Add(self.places_bmp, (1,3))
        iconsz.Add(placesctrl, (2, 3))
        iconsz.Add(self.chat_bmp, (1,4))
        iconsz.Add(chatctrl, (2, 4), (1,1))

        midbelowpanel.SetSizer(iconsz)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        #end below middle panel
    def clientele(self, event):
        Main.Main(self, -1, 'Customers', dbpool)
    def employees(self, event):
        Main.Main(self, -1, 'Employees', dbpool)
    def location(self, event):
        others.Others(self, -1, 'Location', dbpool)
    def Position(self, event):
        others.Others(self, -1, 'Position', dbpool)
    def Agents(self, event):
        others.Others(self, -1, 'Agents', dbpool)
    def sublocation(self, event):
        others.Others(self, -1, 'sublocation', dbpool)
    def Company(self, event):
        others.Others(self, -1, 'Company', dbpool)
    def accounts(self, event):
        others.Others(self, -1, 'Accounts', dbpool)
    def OnCloseMe(self, event):
        self.Close(True)
    def OnCloseWindow(self, event):
        others.Others.OnExit
        Main.Main.OnClose
        self.Destroy()
class IProtocolAvatar(Interface):
    def logout():
        """ Clean up per-login resources allocated to this avatar. """
class EchoAvatar(object):
    implements(IProtocolAvatar)
    def logout(self):
        pass
class Echo(basic.LineReceiver, protocol.Protocol):
    portal = None
    avatar = None
    logout = None

    def __init__(self, factory):
        self.factory = factory
        self.name = None
    def connectionLost(self, reason):
        if self.logout:
            self.logout()
            self.avatar = None
            self.avatarId = None
            self.logout = None
        self.factory.count -= 1
        if self.name in self.factory.users:
            del self.factory.users[self.name]
            self.broadcastMessage("%s has left the channel." % (self.name,))
    def connectionMade(self):
        self.factory.count += 1
    def lineReceived(self, line):
        if not self.avatar:
            username, password = line.strip().split(",")
            self.tryLogin(username, password)
            self.name = username
##            print password
        else:
            self.respondClient(line)
            self.insertSql(line)
    def registerSession(self):
        ip = str(self.transport.getPeer())
        ipinfo = ip.split(',')
        ipv = ipinfo[1]
        print ipv.strip(' ')
        dbpool.runQuery("insert into session (ip_addr, credentials_user_id, date) values (%s, (select user_id from credentials where username = %s ), %s)",(ipv.strip(' '), self.name, time.time()))

    def respondClient(self, line):
        self.handle_CHAT(line)
    def tryLogin(self, username, password):
##        self.portal.login(credentials.UsernamePassword(username, password), None, IProtocolAvatar).addCallbacks(self._cbLogin, self._ebLogin)
        self.portal.login(credentials.UsernameHashedPassword(username, hash(password)), None, IProtocolAvatar).addCallbacks(self._cbLogin, self._ebLogin)
    def _cbLogin(self, (interface, avatar, avatarId, logout)):
        self.avatar = avatar
        self.logout = logout
        self.registerSession()
        self.avatarId = avatarId
        self.factory.users[avatarId] = self
##        self.factory.users.append(self.name)
        self.sendLine("Login successful , please proceed %s. %d clients connected" % (self.name, self.factory.count))
        self.broadcastMessage("%s has joined the channel." % (avatarId,))

    def _ebLogin(self, failure):
        self.sendLine("Login denied, goodbye.")
        self.transport.loseConnection()
    def handle_CHAT(self, message):
        message = "<%s> %s" % (self.name, message)
        print message
        print time.asctime()
        self.broadcastMessage(message)
    def broadcastMessage(self, message):
        for name, protocol in self.factory.users.iteritems():
            if protocol != self:
                protocol.sendLine(message)
    def insertSql(self, line):
        dbdata = line.split(' ')
        if dbdata[0] == 'mita':
            # 8
            #mita 123 1 1 1 20150303   12-3-1013
            try:
                dbpool.runQuery("insert into meter_readings values (%s,%s,%s,%s,%s,%s,%s, %s)", (None, time.time(), dbdata[1],dbdata[2],dbdata[3],dbdata[4],dbdata[5],time.time()))
            except Exception:
                print 'database insertion error'
        elif dbdata[0] == 'quit':
            self.sendLine('Thanks for visiting, ... ending connection in 3...2..1')
            self.transport.loseConnection()
        else:
            pass
class EchoFactory(protocol.Factory):
    count = 0
    def __init__(self, portal, gui):
        self.portal = portal
        self.gui = gui
        self.users = {}
    def buildProtocol(self, addr):
        proto = Echo(self)
        proto.portal = self.portal
        return proto
class Realm(object):
    implements(portal.IRealm)
    def requestAvatar(self, avatarId, mind, *interfaces):
        if IProtocolAvatar in interfaces:
            avatar = EchoAvatar()
            name = str(avatarId)
            return IProtocolAvatar, avatar, avatarId, avatar.logout
        raise NotImplementedError("This realm only supports the IProtocolAvatar interface.")
if __name__ == '__main__':
    realm = Realm()
    myPortal = portal.Portal(realm)
    ##checker = checkers.InMemoryUsernamePasswordDatabaseDontUse()
    from twisted.enterprise import adbapi
    from db_checker import DBCredentialsChecker
    dbpool = adbapi.ConnectionPool("MySQLdb", dbreg.mysql_conn['host'], dbreg.mysql_conn['user'], dbreg.mysql_conn['password'], dbreg.mysql_conn['dbname'], cp_reconnect = True)
    checker = DBCredentialsChecker( dbpool.runQuery, query="SELECT username, password FROM credentials WHERE username = %s")
    ##checker.addUser("user", "pass")
    myPortal.registerChecker(checker)
    app = wx.App(False)
    frame = MainGui(parent=None, id=-1)
    frame.Show()
    reactor.registerWxApp(app)
    reactor.listenTCP(14400, EchoFactory(myPortal, frame))
    reactor.run()

##if __name__ == '__main__':
##    app = wx.App()
##    frame = MainGui(parent=None, id=-1)
##    frame.Show()
##    app.MainLoop()db