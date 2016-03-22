#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Starlord
#
# Created:     30/08/2015
# Copyright:   (c) Starlord 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from twisted.internet import protocol, reactor
class Client(protocol.Protocol):
    def connectionMade(self):
        self.transport.write("San Adreas hehe")
    def dataReceived(self, data):
        print "Server said:", data
        self.transport.loseConnection()

class ClientFactory(protocol.ClientFactory):
    def buildFactory():
        return Client()
    def clientConnectionFailed(self, connector, reason):
        print "Connection failed."
        reactor.stop()
    def clientConnectionLost(self, connector, reason):
        print "Connection lost."
        reactor.stop()
reactor.connectTCP("localhost", 8000, ClientFactory())
reactor.run()
