import os

os.environ['PYTHON_EGG_CACHE'] = '/var/cache/fedoracommunity/egg_cache'

from paste.deploy import loadapp
application = loadapp('config:/srv/fedoracommunity/production.ini')
