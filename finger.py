#!/usr/bin/env python
"""
Twitter fingerer.
"""

from twisted.internet import protocol, reactor, defer, utils
from twisted.protocols import basic
from twisted.web import client

class FingerProtocol(basic.LineReceiver):
    """Finger protocol handler."""

    def getUser(self, u):
        d = defer.Deferred()
        reactor.callWhenRunning(d.callback, "hi")
        return d

    def _formatResponse(self, res):
        self.transport.write(repr(res))
        self.transport.loseConnection()

    def lineReceived(self, user):
        """What to do when a line comes in."""
        d=self.getUser(user)
        d.addErrback(lambda x: self.transport.write("Error:  %s\n" % repr(x)))
        d.addCallback(self._formatResponse)

class FingerFactory(protocol.ServerFactory):
    """Factory for building finger instances"""
    protocol = FingerProtocol

if __name__ == '__main__':
    reactor.listenTCP(1079, FingerFactory())
    reactor.run()
