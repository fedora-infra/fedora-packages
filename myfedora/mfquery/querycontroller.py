from turbogears import controllers, expose
from turbogears import redirect

from koji_query import KojiQuery
from bodhi_query import BodhiQuery

class QueryController(controllers.Controller):
    koji = KojiQuery()
    bodhi = BodhiQuery()
