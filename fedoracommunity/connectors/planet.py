"""
:mod:`fedoracommunity.connectors.planet` - Fedora Planet Connector
==================================================================

This Connector fetches, parses, and caches Fedora's Planet configuration.
This data allows us to query by username and get links to their feeds
and hackergochis.

.. moduleauthor:: Luke Macken <lmacken@redhat.com>
"""

import re
import urllib2

from StringIO import StringIO
from ConfigParser import RawConfigParser
from beaker.cache import Cache
from moksha.connector import IConnector, ICall, IQuery, ParamFilter

planet_cache = Cache('planet')

class PlanetConnector(IConnector):

    @classmethod
    def register(cls):
        pass

    def get_user_details(self, username):
        return planet_cache.get_value(key=username, expiretime=86400,
                createfunc=lambda: self._get_user_details(username))

    def _get_user_details(self, username):
        users = {}
        ini = urllib2.urlopen('http://fedorapeople.org/people_planet.ini')

        for section in ini.read().split('\n\n'):
            match = re.findall('^# Origin: /home/fedora/(.*)/\.planet\n',
                               section)
            if match:
                user = match[0]
                users[user] = {}
                parser = RawConfigParser()
                parser.readfp(StringIO(section))
                sections = parser.sections()
                if sections:
                    feed = sections[0]
                    users[user]['feed'] = feed
                    if parser.has_option(feed, 'name'):
                        users[user]['name'] = parser.get(feed, 'name')
                    if parser.has_option(feed, 'face'):
                        users[user]['face'] = parser.get(feed, 'face')
                    planet_cache.set_value(user, users[user])

        return users.get(username)
