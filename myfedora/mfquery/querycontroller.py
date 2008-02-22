from turbogears import controllers, expose
from turbogears import redirect

from koji_query import KojiReleaseTagsQuery, KojiFilesQuery, KojiGetErrorLogQuery

class QueryController(controllers.Controller):
    koji_tags = KojiReleaseTagsQuery()
    koji_files = KojiFilesQuery()
    koji_get_error_log = KojiGetErrorLogQuery()
