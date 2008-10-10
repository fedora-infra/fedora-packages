from searchbase import SearchBaseWidget
from fedora.client import ProxyClient
import time
import tg
import pylons
from Cookie import SimpleCookie
from myfedora.lib.app_factory import AppFactory
from myfedora.plugins.identity import bloginfo
from myfedora.lib.utils import HRElapsedTime

FULL_WEIGHT=100
MEDIUM_WEIGHT=50
LIGHT_WEIGHT=25

searchurl = 'https://admin.fedoraproject.org/accounts'

class SearchPeopleToolApp(AppFactory):
    entry_name = "tools.searchpeople"
    
class FasClient(ProxyClient):
    visit_name = 'tg-visit'
    
    def __init__(self, baseURL, visit_cookie=None):
        super(FasClient, self).__init__(baseURL)
        self.visit_cookie = visit_cookie

    def user_list(self, search):
        input={'search': search}

        return self.send_request("user/list", 
                                 req_params=input, 
                                 auth_params={'cookie': self.visit_cookie})

def weighted_sort(a, b):
    result = 0
    (a_name, a_weight) = (a[0]['username'], a[1])
    (b_name, b_weight) = (b[0]['username'], b[1])

    result = -cmp(a_weight, b_weight)
    if result == 0:
        result = cmp(a_name, b_name)

    return result

class SearchPeopleToolWidget(SearchBaseWidget):
    params=['search_string', 'results']
    template = 'genshi:myfedora.plugins.apps.tools.templates.searchpeople'
    display_name = 'People'
    requires_auth = True
    
    def search(self, search_terms, timeout_in_seconds=5):
        start_time = time.time()
        
        # use fas to get a list of names but you need to be logged in
        sc = SimpleCookie()
        for key, value in  pylons.request.cookies.iteritems():
            sc[key] = value
            
        fas_client = FasClient('https://admin.fedoraproject.org/accounts/',
                               sc)
        
        st = [search_terms]
        split = search_terms.split()
        
        if len(split) > 1:
            st.extend(split)
            
        search_terms = st
        
        search_results = {} 
        for term in search_terms:
            search = fas_client.user_list('*' + term + '*')

            cmp_term = term.upper()
            hash = search
            if type(search) == tuple:
                hash = search[1]
                
            for user_map in hash['people']:
                user = user_map['username']
                name = user_map['human_name']
                if not name:
                    name = ''
                cmp_user = user.upper()
                cmp_name = name.upper()

                result = search_results.get(user, None)

                if not result:
                    result = [user_map, 0]

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
                    if cmp_user.count(cmp_term):
                        count += 1

                    if cmp_name.count(cmp_term):
                        count += 1

                    if count > 1:
                        relevance += FULL_WEIGHT * (count / len(search_terms))

                # if we start with one of the search terms
                # add weight to the relevance
                if cmp_user.startswith(cmp_term):
                    relevance += LIGHT_WEIGHT
                
                if cmp_name.startswith(cmp_term):
                    relevance += LIGHT_WEIGHT

                # if we end with one of the seach terms
                # add weight to relevance
                if cmp_user.endswith(cmp_term):
                    relevance += LIGHT_WEIGHT

                if cmp_name.endswith(cmp_term):
                    relevance += LIGHT_WEIGHT

                result[1] = relevance
                search_results[user] = result
            
            # if we go over the timeout exit so we don't 
            # take too much time to return a result
            if (time.time() - start_time) > timeout_in_seconds:
                break

        weighted_user_list = search_results.values()
        weighted_user_list.sort(weighted_sort)
        
        user_list = []
        for user in weighted_user_list:
            user_name = user[0]['username']
            
            item = {'url': tg.url('/people/name/' + user_name),
                    'weight': user[1],
                    'widget_id': self.id}
            
            # get hackergotchi
            b = bloginfo.get_metadata(user_name)
            if b:
                item.update(b)
                
            # calc time
            hret = HRElapsedTime()
            hret.set_start_timestr(user[0]['last_seen'])
            hret.set_end_time_to_now()
            line0 = hret.get_hr_elapsed_time()
            line1 = hret.get_hr_start_time()
                
            item.update({'last_seen_hr_0':line0,'last_seen_hr_1':line1})
                
            item.update(user[0])
            user_list.append(item)

        return user_list
