"""The application's Globals object"""

from app_factory import AppFactoryDict

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application
    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the 'g'
        variable
        """
        self.widgets = {'home': {}, 'canvas': {}, 'profile': {}, 'preview': {}, 'config':{}} # {viewtype: {name: Widget instance}}
        self.resourceviews = AppFactoryDict() # {name: ResourceView instance}
        self.apps =  AppFactoryDict() # {name: App instance}

        # Our comet data streamer, responsible for polling the data
        # streams, and providing data to the widgets
        #from myfedora.streams import DataStreamer
        #self.datastreamer = DataStreamer()

        #FEED_CACHE = "/tmp/moksha-feeds"

        #from shove import Shove
        #from feedcache.cache import Cache
        #self.feed_storage = Shove('file://' + FEED_CACHE)
        #self.feed_cache = Cache(self.feed_storage)
