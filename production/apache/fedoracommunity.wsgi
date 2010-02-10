import os
os.environ['PYTHON_EGG_CACHE'] = '/var/cache/fedoracommunity/.egg_cache'
import __main__
__main__.__requires__ = 'fedoracommunity'
import pkg_resources

from paste.deploy import loadapp
application = loadapp('config:/etc/fedoracommunity/production.ini')

