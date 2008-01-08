class URLHandler:
    def __init__(self):
        self.set_base_url('')

    def set_base_url(self, url):
        if not url.endswith('/'):
            url = url + '/'

        self.base_url = url

    def get_base_url(self):
        return self.base_url

    def get_package_url(self, pkg_name):
        return self.get_base_url() + pkg_name
