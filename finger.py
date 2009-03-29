#!/usr/bin/env python
"""
Twitter fingerer.
"""

import sys

sys.path.insert(0, 'twitty-twister/lib')

from twisted.internet import protocol, reactor, defer, utils
from twisted.protocols import finger
from twisted.python import log
from twisted.web import client

import twitter

class FingerProtocol(finger.Finger):
    """Finger protocol handler."""

    def getUser(self, slash_w, user):
        d = twitter.Twitter().show_user(user)
        d.addCallback(self._formatResponse)
        d.addErrback(log.err)
        d.addErrback(lambda e: self._refuseMessage(str(e)))

    def _formatResponse(self, res):
        s = """Login: %(login)s         			Name: %(name)s

%(status)s
""" % {'login': res.screen_name, 'name': res.name, 'status': res.status.text}
        self._refuseMessage(s.encode('utf-8'))

class FingerFactory(protocol.ServerFactory):
    """Factory for building finger instances"""
    protocol = FingerProtocol
