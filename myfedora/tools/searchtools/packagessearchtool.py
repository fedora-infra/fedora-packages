from myfedora.plugin import Tool
from turbogears import expose

import os
import koji

from myfedora.urlhandler import KojiURLHandler
from locale import strcoll

FULL_WEIGHT=100
MEDIUM_WEIGHT=50
LIGHT_WEIGHT=25

# sort based on weight, each element is of the form [package_name, weight]
def weighted_sort(a, b):
    result = 0
    (a_name, a_weight) = a
    (b_name, b_weight) = b

    result = -cmp(a_weight, b_weight)
    if result == 0:
        result = cmp(a_name, b_name)

    return result

class PackageSearchTool(Tool):
    def __init__(self, parent_resource):
        Tool.__init__(self, parent_resource,
                                   'Packages',
                                   'packages',
                                   'Fedora package search',
                                   '''Searches the Fedora package database''',
                                   ['search'],
                                   [])

    @expose(template='myfedora.tools.searchtools.templates.index', allow_json=True)
    def index(self, search_string='', **kwargs):
        result = self.get_parent_resource().get_template_globals(search_string)

        return result

    def search(self, search_str):
        # use koji for now but we really should use pkgdb 
        # or better yet set up a search db 
        cs = koji.ClientSession(KojiURLHandler().get_xml_rpc_url())
        search_terms = search_str.split()
        search_results = {} 
        for term in search_terms:
            search = cs.search('*' + term + '*', 'package', 'glob')
            cmp_term = term.upper()
            for pkg_hash in search:
                pkg = pkg_hash['name']
                cmp_pkg = pkg.upper()

                result = search_results.get(pkg, None)

                if not result:
                    result = [pkg, 0]

                relevance = result[1]

                # if we found this more than once 
                # then add weight to it's relevance 
                if relevance > 0:
                    relevance += MEDIUM_WEIGHT

                # if all search terms are in then
                # add weight to the relevance
                for check_term in search_terms:
                    count = 0
                    cmp_check_term = check_term.upper()
                    if cmp_pkg.count(cmp_term):
                        count += 1

                    if count > 1:
                        relevance += FULL_WEIGHT * (count / len(search_terms))

                # if we start with one of the search terms
                # add weight to the relevance
                if cmp_pkg.startswith(cmp_term):
                    relevance += LIGHT_WEIGHT

                # if we end with one of the seach terms
                # add weight to relevance
                if cmp_pkg.endswith(cmp_term):
                    relevance += LIGHT_WEIGHT

                result[1] = relevance
                search_results[pkg] = result

        weighted_pkg_list = search_results.values()
        weighted_pkg_list.sort(weighted_sort)
        
        pkg_list = []
        # put it into the form we want
        # FIXME: we can optimize above so we don't have to do this
        for pkg in weighted_pkg_list:
            item = {'name': pkg[0],
                    'url': self.get_parent_resource().url('/packages/' + pkg[0]),
                    'summary': '' }# none for now
            pkg_list.append(item)

        return pkg_list

    # need to do this in order to get back non html formatted data 
    def _raw_results(self, search_string):
        parent = self.get_parent_resource()  
        
        items = self.search(search_string)
              
        result_hash = {'header': self.get_display_name(),
                       'url': parent.cat_tool_url(self.get_id(),
                                                  search_string),
                       'items':items
                      }

        search_results = [result_hash]
       
        return search_results

    @expose(template='myfedora.tools.searchtools.templates.results', allow_json=True)
    def results(self, search_string=''):
        parent = self.get_parent_resource()
        result = parent.get_template_globals(search_string)
        result.update(self._raw_results())

        return result 
