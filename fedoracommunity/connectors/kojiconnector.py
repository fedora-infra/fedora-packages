from moksha.connector import IConnector, ICall, IQuery
from pylons import config
import koji 

class KojiConnector(IConnector, ICall, IQuery):
    def __init__(self):
        self._koji_client = koji.ClientSession(self._base_url)
    
    # IConnector
    @classmethod
    def register(cls):
        cls._base_url = config.get('fedoracommunity.connector.kojihub.baseurl',
                                   'http://koji.fedoraproject.org/kojihub')
        
        cls.register_query_builds()
                                                                  
    def request_data(self, resource_path, params, _cookies):
        return self._koji_client(**params)
    
    def introspect(self):
        # FIXME: return introspection data
        return None
    
    #ICall
    def call(self, resource_path, params, _cookies):
        # koji client only returns structured data so we can pass
        # this off to request_data
        return self.request_data(resource_path, params, _cookies)
        
    #IQuery
    def query(self, resource_path, params, _cookies, 
              offset = 0, 
              num_rows = 10,
              sort_col = None,
              sort_order = -1,
              filters = {}):
        
        results = None
        r = {
              "total_rows": 0, 
              "row_count": 0,   
              "offset": 0,   
              "rows": None
            }
        
        if not sort_col:
            sort_col = self.get_default_sort_col(resource_path)
          
        if resource_path == 'query_builds':
            if params == None:
                params = {}
                
            (total_rows, rows) = self.query_builds(offset = offset, 
                                                   limit = num_rows,
                                                   order = sort_order,
                                                   sort_col = sort_col,
                                                   filters = filters, 
                                                   **params)
            r['total_rows'] = total_rows
            r['row_count'] = len(rows)
            if offset:
                r['offset'] = offset
            r['rows'] = rows
            
            results = r
        
        return results
        
    # KojiConnector
    @classmethod
    def register_query_builds(cls):
        cls.register_path(
                      'query_builds', 
                      primary_key_col = 'build_id',
                      default_sort_col = 'build_id',
                      default_sort_order = -1,
                      can_paginate = True)
        
        cls.register_column('query_builds', 'build_id', 
                        default_visible = True, 
                        can_sort = True, 
                        can_filter_wildcards = False)
        cls.register_column('query_builds', 'nvr', 
                        default_visible = True, 
                        can_sort = True, 
                        can_filter_wildcards = False)
        cls.register_column('query_builds', 'owner_name', 
                        default_visible = True, 
                        can_sort = True, 
                        can_filter_wildcards = False)
        cls.register_column('query_builds', 'state', 
                        default_visible = True, 
                        can_sort = True, 
                        can_filter_wildcards = False)
        
    def query_builds(self, offset=None,
                           limit=None, 
                           order=-1,
                           sort_col=None,
                           filters = {},
                           **params):
        
        # FIXME: make filter an object
        user = filters.get('user', '')
        if isinstance(user, dict):
            user = user['value']
                
        package = filters.get('package', '')
        if isinstance(package, dict):
            package = package['value']
            
        state = filters.get('state')
        if isinstance(state, dict):
            state = state['value']
        
        complete_before = None
        complete_after = None
        completed_filter = filters.get('completed')
        if completed_filter:
            if completed_filter['op'] in ('>', 'after'):
                complete_after = completed_filter['value']
            elif completed_filter['op'] in ('<', 'before'):
                complete_before = completed_filter['value']
        
        if order < 0:
            order = '-' + sort_col
        else:
            order = sort_col
        
        user = self._koji_client.getUser(user)
        
        id = None
        if user:
            id = user['id']

        pkg_id = None
        if package:
            pkg_id = self._koji_client.getPackageID(package)

        queryOpts = None
        
        if state:
            state = int(state)
        
        qo = {}
        if not offset == None:
          qo['offset'] = int(offset)
          
        if not offset == limit:
            qo['limit'] = int(limit)
            
        if order:
            qo['order'] = order
            
        if qo:
            queryOpts = qo
            
        countQueryOpts = {'countOnly': True}
        
        self._koji_client.multicall = True
        self._koji_client.listBuilds(packageID=pkg_id,
                      userID=id,
                      state=state,
                      completeBefore = complete_before,
                      completeAfter = complete_after,
                      queryOpts=countQueryOpts)
        
        self._koji_client.listBuilds(packageID=pkg_id,
                      userID=id,
                      state=state,
                      completeBefore = complete_before,
                      completeAfter = complete_after,
                      queryOpts=queryOpts)
        
        results = self._koji_client.multiCall()
        builds_list = results[1][0]
        total_count = results[0][0]
        
        self._koji_client.multicall = False
                
        return (total_count, builds_list)
