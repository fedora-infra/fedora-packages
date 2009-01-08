"""The application's Globals object"""

from tg import config
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
