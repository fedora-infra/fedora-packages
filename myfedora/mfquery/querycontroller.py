from turbogears import controllers, expose
from turbogears import redirect

from koji_query import KojiReleaseTagsQuery

class QueryController(controllers.Controller):
    koji_tags = KojiReleaseTagsQuery()
