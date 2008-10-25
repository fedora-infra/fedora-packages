import os

os.environ['PYTHON_EGG_CACHE'] = '/var/cache/myfedora/egg_cache'

from paste.deploy import loadapp
application = loadapp('config:/etc/myfedora/myfedora.ini')
