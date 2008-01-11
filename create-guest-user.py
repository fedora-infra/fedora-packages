#!/usr/bin/python -tt

from turbogears import update_config
from turbogears.database import PackageHub
from myfedora.model import User, Group

update_config(configfile='dev.cfg', modulename='myfedora.config') 
hub = __connection__ = PackageHub("bodhi")
hub.begin()
guest = User(user_name='guest', display_name='Guest User',
             email_address="nobody@fedoraproject.org", password="guest")
hub.commit()

print guest
print "Guest user created!"
