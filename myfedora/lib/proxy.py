from fedora.client import ProxyClient
from Cookie import SimpleCookie
from pylons import request

def convert_to_simple_cookie(cookie):
    sc = SimpleCookie()
    for key, value in cookie.iteritems():
        sc[key] = value
            
    return sc

class FasClient(ProxyClient):
    def __init__(self, baseURL='https://admin.fedoraproject.org/accounts'):
        super(FasClient, self).__init__(baseURL)
    
    def get_user_info(self, user, full_results=False):
        cookies = request.cookies
        cookies = convert_to_simple_cookie(cookies)
        auth_params = {'cookie': cookies}
        result = self.send_request('user/view/' + user, 
                                    auth_params = auth_params)
        
        if full_results:
            return result
        else:
            if len(result) > 1:
                return result[1]
            else:
                return result[0]