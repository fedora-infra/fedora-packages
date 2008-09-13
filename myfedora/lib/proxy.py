from fedora.client import ProxyClient
from Cookie import SimpleCookie
from pylons import request

class MFProxyClient(ProxyClient):
    def __init__(self, base_url, useragent=None, debug=False, return_auth=False):
        super(MFProxyClient, self).__init__(base_url, 
                                            useragent=useragent, 
                                            debug=debug)
        self._return_auth = return_auth
        
    def convert_to_simple_cookie(self, cookie):
        sc = SimpleCookie()
        for key, value in cookie.iteritems():
            sc[key] = value
            
        return sc

    def get_current_proxy_cookies(self):
        cookies = request.cookies
        cookies = self.convert_to_simple_cookie(cookies)
        return cookies
    
    def send_authenticated_request(self, method, req_params=None):
        auth_params = {'cookie': self.get_current_proxy_cookies()}
        result = self.send_request(method,
                                   req_params = req_params,
                                   auth_params = auth_params)
        
        if not self._return_auth:
            result = result[1]
            
        return result

class FasClient(MFProxyClient):
    def __init__(self, baseURL='https://admin.fedoraproject.org/accounts'):
        super(FasClient, self).__init__(baseURL)
    
    def get_user_info(self, user, full_results=False):
        result = self.send_authenticated_request('user/view/' + user)
        
        return result
    
class PkgdbClient(MFProxyClient):
    def __init__(self, baseURL='https://admin.fedoraproject.org/pkgdb'):
        super(PkgdbClient, self).__init__(baseURL)
        
    def get_package_info(self, name):
        result = self.send_authenticated_request("packages/name", 
                                               req_params={'packageName': name})
        
        return result
    
    def get_user_packages(self, user):
        result = self.send_authenticated_request("users/packages/" + user)
        
        return result