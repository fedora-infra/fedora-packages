from moksha.lib.helpers import CategoryEnum

def LinkData(object):
    def __init__(_link, **kwds):
        self._link = link
        self._params = kwds

    def get_link(self):
        return self._link

    def get_params(self, d = None):
        params = self._params
        if d:
            params = {}
            for p in self._params:
                params[p] = d.get(p, self._params[p])
                if params[p] == None:
                    del params[p]

        return params

builds_links = CategoryEnum('build_link',
                             ('PACKAGE',
                              '/package_maint/packages/package'
                             ),
                             ('ALL_BUILDS',
                              '/package_maint/builds'
                             )
                           )
