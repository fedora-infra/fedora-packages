"""Test Secure Controller"""
from testtg.lib.base import BaseController, SecureController
from tg import expose, flash
from pylons.i18n import ugettext as _
#from tg import redirect, validate
#from testtg.model import DBSession, metadata
#from dbsprockets.dbmechanic.frameworks.tg2 import DBMechanic
#from dbsprockets.saprovider import SAProvider
from tg.ext.repoze.who import authorize


class Secc(SecureController):

    require = authorize.has_permission('manage')

    @expose('testtg.templates.index')
    def index(self):
        flash(_("Secure Controller here"))
        return dict(page='index')

    @expose('testtg.templates.index')
    def some_where(self):
        """should be protected because of the require attr
        at the controller level.
        """
        return dict()

