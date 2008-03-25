from turbogears import controllers, expose
from turbogears import redirect

from koji_query import KojiQuery


class QueryController(controllers.Controller):
    koji = KojiQuery()
