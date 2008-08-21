from searchbase import SearchBaseWidget
from fedora.tg.client import BaseClient
import time
import tg

FULL_WEIGHT=100
MEDIUM_WEIGHT=50
LIGHT_WEIGHT=25

searchurl = 'https://admin.fedoraproject.org/pkgdb'

# sort based on weight, each element is of the form [package_name, weight]
def weighted_sort(a, b):
    result = 0
    (a_name, a_weight) = a
    (b_name, b_weight) = b

    result = -cmp(a_weight, b_weight)
    if result == 0:
        result = cmp(a_name, b_name)

    return result

class PkgdbClient(BaseClient):
    def search(self, search_term):
        return self.send_request("search/package", req_params={'searchwords': search_term})

class SearchPackagesToolWidget(SearchBaseWidget):
    params=['search_string', 'results']
    template = 'genshi:myfedora.plugins.apps.tools.templates.searchpackages'
    display_name = 'Packages'
    
    def search(self, search_terms, timeout_in_seconds=5):
        results = []
        start_time = time.time()
    
        client = PkgdbClient(searchurl)
    
        st = [search_terms]
        split = search_terms.split()
        
        if len(split) > 1:
            st.extend(split)
        search_terms = st
        
        search_results = {} 
        for term in search_terms:
            search =  client.search(term)
            cmp_term = term.upper()
            for pkg_hash in search['packages']:
                pkg_name = pkg_hash['name']
                cmp_pkg = pkg_name.upper()

                result = search_results.get(pkg_name, None)

                if not result:
                    result = [pkg_hash, 0]

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

                # if we end with one of the search terms
                # add weight to relevance
                if cmp_pkg.endswith(cmp_term):
                    relevance += LIGHT_WEIGHT

                result[1] = relevance
                search_results[pkg_name] = result
            
            # if we go over the timeout exit so we don't 
            # take too much time to return a result
            if (time.time() - start_time) > timeout_in_seconds:
                break

        weighted_pkg_list = search_results.values()
        weighted_pkg_list.sort(weighted_sort)
        
        pkg_list = []
        # put it into the form we want
        # FIXME: we can optimize above so we don't have to do this
        for pkg in weighted_pkg_list:
            pkg_hash = pkg[0]
            pkg_hash.update({'url': tg.url('/packages/name/' + pkg_hash['name']),
                             'weight': pkg[1],
                             'widget_id': self.id})
            item = pkg_hash
                                  
            pkg_list.append(item)

        results = pkg_list
    
        return results
    