import os
os.environ['PYTHON_EGG_CACHE'] = '/var/cache/fedoracommunity/.egg_cache'
import __main__
__main__.__requires__ = 'fedoracommunity'
import pkg_resources

APP_CONFIG = '/etc/fedoracommunity/production.ini'

import logging.config
logging.config.fileConfig(APP_CONFIG)

from paste.deploy import loadapp
application = loadapp('config:%s' % APP_CONFIG)

