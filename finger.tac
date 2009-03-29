import sys
sys.path.insert(0, "twitty-twister/lib")

from twisted.application import service
from twisted.internet import reactor
import twitter
import finger

# Set the user agent for twitter
twitter.Twitter.agent = "fingerspy"

application = service.Application("finger")

reactor.listenTCP(1079, finger.FingerFactory())
