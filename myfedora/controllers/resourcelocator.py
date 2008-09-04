from myfedora.lib.base import BaseController
from tg import expose, redirect, url
import pylons

class ResourcelocatorController(BaseController):
    def __init__(self):
        super(ResourcelocatorController, self).__init__()

    @expose()
    def lookup(self, *args):
        resource = args[0]
        base_path = url('/').split('/')
        my_path = list(args)        

        if base_path:
            if not base_path[0]:
                base_path.pop(0)

            for el in base_path:
                if el == args[0]:
                    my_path.pop(0)
                else:
                    break;
          
        resource = my_path[0]

        # if we don't have a slash at the end redirect to it so relative links work 
        last_arg = my_path[-1]
        if last_arg:
            path = url(pylons.request.environ.get('PATH_INFO')) + '/'
            redirect(path)
        
        r = pylons.app_globals.resourceviews.get(resource, None)
    
        if r:
            if len(my_path) == 1 or not my_path[1]:
                return r.controller, []
        
            return r.controller, my_path