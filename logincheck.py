#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Starlord
#
# Created:     09/09/2015
# Copyright:   (c) Starlord 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from zope.interface import implements, Interface
from twisted.cred import checkers, credentials, portal
from twisted.internet import protocol, reactor
from twisted.protocols import basic
import time
import hashlib
def hash(password):
    return hashlib.md5(password).hexdigest()
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
    def __init__(self, portal):
        self.portal = portal
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
realm = Realm()
myPortal = portal.Portal(realm)
##checker = checkers.InMemoryUsernamePasswordDatabaseDontUse()
from twisted.enterprise import adbapi
from db_checker import DBCredentialsChecker
dbpool = adbapi.ConnectionPool("MySQLdb", 'localhost', 'root', 'modulator', 'mita', cp_reconnect = True)
checker = DBCredentialsChecker( dbpool.runQuery, query="SELECT username, password FROM credentials WHERE username = %s")
##checker.addUser("user", "pass")
myPortal.registerChecker(checker)
reactor.listenTCP(14400, EchoFactory(myPortal))
reactor.run()