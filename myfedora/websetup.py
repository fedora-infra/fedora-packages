"""Setup the myfedora application"""
import logging

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

    u = model.User()
    u.user_name = u'manager'
    u.display_name = u'Exemple manager'
    u.email_address = u'manager@somedomain.com'
    u.password = u'managepass'

    model.DBSession.save(u)

    g = model.Group()
    g.group_name = u'managers'
    g.display_name = u'Managers Group'

    g.users.append(u)

    model.DBSession.save(g)

    p = model.Permission()
    p.permission_name = u'manage'
    p.description = u'This permission give an administrative right to the bearer'
    p.groups.append(g)

    model.DBSession.save(p)
    model.DBSession.flush()

    u1 = model.User()
    u1.user_name = u'editor'
    u1.display_name = u'Exemple editor'
    u1.email_address = u'editor@somedomain.com'
    u1.password = u'editpass'

    model.DBSession.save(u1)
    model.DBSession.flush()

    model.DBSession.commit()
    print "Successfully setup"
