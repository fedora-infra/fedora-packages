from basesearch import BaseSearch

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

class PackageSearch(BaseSearch):
    def __init__(self):
        BaseSearch.__init__(self)
        self.set_search_shortcut('pkg')

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

        pkg_list = search_results.values()
        pkg_list.sort(weighted_sort)
        
        return pkg_list

