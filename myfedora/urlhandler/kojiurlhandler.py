from urlhandler import URLHandler

import koji

class KojiURLHandler(URLHandler):
    def __init__(self):
        URLHandler.__init__(self)

        self.set_base_url('http://koji.fedoraproject.org/')

        self.package_path = 'koji/packageinfo?packageID='
        self.xml_rpc_path = 'kojihub'

    def get_package_url(self, pkg_name):
        cs = koji.ClientSession(self.get_base_url() + self.xml_rpc_path)
        pkg = cs.getPackage(pkg_name)

        return self.get_base_url() + self.package_path + str(pkg['id'])
