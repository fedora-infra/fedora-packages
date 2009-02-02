"""Setup the myfedora application"""
import logging

import transaction
from paste.deploy import appconfig
from pylons import config

from myfedora.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_config(command, filename, section, vars):
    """Place any commands to setup myfedora here"""
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)
    # Load the models
    from myfedora import model
    print "Creating tables"
    model.metadata.create_all(bind=config['pylons.app_globals'].sa_engine)

    #u.user_name = u'manager'
    #u.display_name = u'Exemple manager'
    #u.email_address = u'manager@somedomain.com'
    #u.password = u'managepass'

    #model.DBSession.save(u)

    #transaction.commit()
    print "Successfully setup"
