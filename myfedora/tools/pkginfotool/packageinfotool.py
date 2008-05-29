from myfedora.plugin import Tool
from turbogears import expose
from fedora.tg.client import BaseClient

class PkgdbClient(BaseClient):
    def packages_name(self, name):
        return self.send_request("packages/name", input={'packageName': name})

class PackageInfoTool(Tool):
    def __init__(self, parent_resource):
        Tool.__init__(self, parent_resource,
                                   'Info',
                                   'info',
                                   'Shows information about a package',
                                   '''This tool is tied to the package resource
                                   and is used for getting basic information
                                   about a package.
                                   ''',
                                   ['packages'],
                                   ['packages'])

    @expose(template='myfedora.tools.pkginfotool.templates.info')
    def default(self, package):
        result = self.get_parent_resource().get_template_globals(package)
        pkgdb_client = PkgdbClient('https://admin.fedoraproject.org/pkgdb/')
        json_data = pkgdb_client.packages_name(package)
        result.update({'package': package, 'data': json_data}) 
        return result
