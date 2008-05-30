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

    def _compare_collection_versions(self, a, b):
        result = 0
        if a['name'] == b['name']:
            try:
                af = float(a['version']) 
                bf = float(b['version'])

                result = int(af - bf)
            except:
                if a['version'] > b['version']:
                    result = 1
                elif a['version']  < b['version']:
                    result = -1
        else:
            if a['name'] == 'Fedora':
                result = 1
            elif b['name'] == 'Fedora':
                result = -1
            elif a['name'] > b['name']:
                result = 1
            elif b['name'] > a['name']:
                result = -1

        # we want decending
        return -result

    @expose(template='myfedora.tools.pkginfotool.templates.info')
    def default(self, package):
        result = self.get_parent_resource().get_template_globals(package)
        pkgdb_client = PkgdbClient('https://admin.fedoraproject.org/pkgdb/')
        json_data = pkgdb_client.packages_name(package)
        
        data = {}
        collection_list = []
        for pd in json_data['packageListings']:
            collection = pd['collection']
            package = pd['package']
            people = pd['people']
            if collection['version'] == 'devel':
                data['description'] =  pd['package']['description']
                data['summary'] =  pd['package']['summary']
            
            c = {}
            c['name'] = collection['name'] 
            c['version'] = collection['version']
            c['fullname'] = c['name'] + ' ' + c['version']
            c['package_owner_id'] = pd['owneruser']

            for p in people:
                c['package_owner_name'] = c['package_owner_id']
                if p['user'] == c['package_owner_id']:
                    c['package_owner_name'] = p['name']
                    break

            collection_list.append(c)
            
        collection_list.sort(self._compare_collection_versions)
        data['collection_list'] = collection_list

        result.update({'package_data': data}) 
        return result
