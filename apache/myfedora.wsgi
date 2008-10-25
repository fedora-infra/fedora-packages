import os, sys
import site

from paste.deploy import appconfig
from pylons import config
from myfedora.config.environment import load_environment

from paste.deploy import loadapp
application = loadapp('config:/etc/myfedora/myfedora.ini')
