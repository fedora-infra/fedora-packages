from turbogears import controllers, expose

from myfedora.urlhandler import KojiURLHandler
import koji

class KojiReleaseTagsQuery(controllers.Controller):
    @expose("json", allow_json=True)
    def index(self, *args, **kw):
        build_id = int(kw.get('build_id', '0'))

        cs = koji.ClientSession(KojiURLHandler().get_xml_rpc_url())

        tags = cs.listTags(build = build_id)

        return {'tags': tags}
