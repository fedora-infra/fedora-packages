from myfedora.lib.base import BaseController
from tg import expose, redirect
import pylons

class ResourcelocatorController(BaseController):
    def __init__(self):
        super(ResourcelocatorController, self).__init__()

    @expose()
    def lookup(self, *args):
        resource = args[0]
        
        # if we don't have a slash at the end redirect to it so relative links work 
        last_arg = args[-1]
        if last_arg:
            path = pylons.request.environ.get('PATH_INFO') + '/'
            redirect(path)
        
        r = pylons.app_globals.resourceviews.get(resource, None)
        
        if r:
            if len(args) == 1 or not args[1]:
                return r.controller, []
        
            return r.controller, list(args)