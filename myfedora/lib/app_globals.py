"""The application's Globals object"""

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
        self.views = {} # {name: View instance}

        # Our comet data streamer, responsible for polling the data
        # streams, and providing data to the widgets
        from myfedora.streams import DataStreamer
        self.datastreamer = DataStreamer()
