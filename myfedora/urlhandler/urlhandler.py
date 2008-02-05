class URLHandler:
    (IFRAME_LINK,   # target link to an iframe 
     INTERNAL_LINK, # target link to the current browser window
     EXTERNAL_LINK) = range(3) # target link to a new browser window 

    def __init__(self):
        self._link_type = self.IFRAME_LINK # default to iframe
        self.set_base_url('http://localhost:8080/')

    def get_link_type(self):
        return self._link_type

    def _set_link_type(self, link_type):
        self._link_type = link_type

    def set_base_url(self, url):
        if not url.endswith('/'):
            url = url + '/'

        self.base_url = url

    def get_base_url(self):
        return self.base_url

    def get_package_url(self, pkg_name):
        return self.get_base_url() + pkg_name
