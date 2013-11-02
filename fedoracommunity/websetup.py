# This file is part of Fedora Community.
# Copyright (C) 2008-2010  Red Hat, Inc.
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

"""Setup the Fedora Community application"""
import logging

import transaction
from paste.deploy import appconfig
from pylons import config

from fedoracommunity.config.environment import load_environment

log = logging.getLogger(__name__)


def setup_config(command, filename, section, vars):
    """Place any commands to setup Fedora Community here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)
    # Load the models
    from fedoracommunity import model
    print "Creating tables"
    model.metadata.create_all(bind=config['pylons.app_globals'].sa_engine)

    #u.user_name = u'manager'
    #u.display_name = u'Exemple manager'
    #u.email_address = u'manager@somedomain.com'
    #u.password = u'managepass'

    #model.DBSession.save(u)

    #transaction.commit()
    print "Successfully setup"
