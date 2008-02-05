from urlhandler import URLHandler

import koji

class KojiURLHandler(URLHandler):
    def __init__(self):
        URLHandler.__init__(self)

        self._set_link_type(self.INTERNAL_LINK)

        self.route = None

        self.package_path = 'packages/'
        self.xml_rpc_path = 'kojihub'
        self.xml_rpc_url = 'http://koji.fedoraproject.org/' + self.xml_rpc_path

    def get_route(self):
        if not self.route:
            from myfedora.packagecontroller.buildsroute import BuildsRoute
            self.route = BuildsRoute()

        return self.route

    def get_package_url(self, pkg_name):
        return self.get_base_url() + self.package_path + pkg_name + '/Builds/'

    def get_xml_rpc_url(self):
        return self.xml_rpc_url
