# This file is part of Fedora Community.
# Copyright (C) 2008-2009  Red Hat, Inc.
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
:mod:`fedoracommunity.connectors.jsonconnector` - Simple Json Connector
=======================================================================

This Connector works with any url which returns valid simplejson data

.. moduleauthor:: Seth Vidal <skvidal@fedoraproject.org>
"""
import logging
log = logging.getLogger(__name__)

from datetime import datetime, timedelta
from pylons import cache
from urlgrabber.grabber import urlread, urlopen, URLGrabError
import simplejson
from moksha.connector import IConnector, ICall, IQuery, ParamFilter

class SimpleJsonConnector(IConnector, ICall, IQuery):
    _method_paths = {}
    _query_paths = {}

    def __init__(self, environ=None, request=None):
        super(SimpleJsonConnector, self).__init__(environ, request)
        # FIXME - sanity check this url or run it past a whitelist or what not
        
    def call(self, url):
        log.info('JsonConnector.call(%s)' % locals())        
        # FIXME - LOTS OF ERROR CHECKING PLEASE
        # grab the json_url
        json_fp = urlopen(url)
        # decode it into python using simplejson
        json_data = simplejson.load(json_fp)
        json_fp.close()
        # return the object you get from it
        return json_data
