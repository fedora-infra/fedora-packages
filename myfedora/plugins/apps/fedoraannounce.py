from moksha.feed import Feed
from myfedora.lib.app_factory import AppFactory

class FedoraAnnounceHomeWidget(Feed):
    link = 'https://www.redhat.com/archives/fedora-announce-list/'
    url = '/misc/fedora_announce.xml'

class FedoraAnnounceCanvasWidget(Feed):
    link = 'https://www.redhat.com/archives/fedora-announce-list/'
    url = '/misc/fedora_announce.xml'
    view = 'canvas'

class FedoraAnnounceApp(AppFactory):
    entry_name = 'fedoraannounce'
