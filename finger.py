#!/usr/bin/env python
"""
Twitter fingerer.
"""

import sys
import string

sys.path.insert(0, 'twitty-twister/lib')

from twisted.internet import protocol, reactor, defer, utils
from twisted.protocols import finger
from twisted.python import log
from twisted.web import client

import twitter

SERVICES = {'twitter': 'http://twitter.com/', 'identi.ca': 'http://identi.ca/api'}
DEFAULT_DOMAIN = 'twitter'

class FingerProtocol(finger.Finger):
    """Finger protocol handler."""

    # Copied this out of twisted's and fixed a stupid bug.
    def lineReceived(self, line):
        parts = string.split(line)
        if not parts:
            parts = ['']
        if len(parts) == 1:
            slash_w = 0
        else:
            slash_w = 1
        user = parts[-1]
        if '@' in user:
            host_place = string.rfind(user, '@')
            u = user[:host_place]
            h = user[host_place+1:]
            return self.forwardQuery(slash_w, u, h)
        if user:
            return self.getUser(slash_w, user)
        else:
            return self.getDomain(slash_w)

    def forwardQuery(self, slash_w, user, host):
        d = twitter.Twitter(base_url=SERVICES[host]).show_user(user)
        d.addCallback(self._formatResponse)
        d.addErrback(log.err)
        d.addErrback(lambda e: self._refuseMessage(str(e)))

    def getUser(self, slash_w, user):
        self.forwardQuery(slash_w, user, DEFAULT_DOMAIN)

    def getDomain(self, slash_w):
        rv = ["The following services are supported:"]

        rv.append('\n'.join([" - " + s for s in SERVICES.keys()]))
        self._refuseMessage("\n".join(rv))

    def _formatResponse(self, res):
        s = """Login: %(login)s         			Name: %(name)s

%(status)s
""" % {'login': res.screen_name, 'name': res.name, 'status': res.status.text}
        self._refuseMessage(s.encode('utf-8'))

class FingerFactory(protocol.ServerFactory):
    """Factory for building finger instances"""
    protocol = FingerProtocol
