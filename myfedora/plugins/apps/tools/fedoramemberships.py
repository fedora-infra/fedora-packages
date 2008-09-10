from pylons import tmpl_context, request

from myfedora.widgets.resourceview import ToolWidget
from myfedora.lib.app_factory import AppFactory
from fedora.client import ProxyClient
from Cookie import SimpleCookie

class FedoraMembershipsToolApp(AppFactory):
    entry_name = "tools.fedoramemberships"

class FedoraMembershipsToolWidget(ToolWidget):
    template = 'genshi:myfedora.plugins.apps.tools.templates.fedoramemberships'
    display_name = "Memberships"

    def group_type_to_name(self, gtype):
        if gtype == 'tracking':
            return 'Fedora Rolls'
        elif (gtype == 'git' or
              gtype == 'svn' or
              gtype == 'bzr' or
              gtype == 'hg'):
            return 'Fedora Hosted Projects'
        elif gtype == 'cvs':
            return 'Fedora Packaging'
        elif gtype == 'shell':
            return 'Fedora Shell Accounts'
        
        return 'Unknown Group Type (%s)' % (gtype)
    def group_membership_data(self, memberships):
        if not memberships: 
            return None
        
        results = {}
        for m in memberships:
            grouping_name = self.group_type_to_name(m['group_type'])
            print m
            if results.has_key(grouping_name):
                results[grouping_name].append(m)
            else:
                results[grouping_name]=[m]
        
        return results
            
    def get_profile_data(self):
        try:
            p = tmpl_context.identity['person']
        
            
            return {'approved_memberships': self.group_membership_data(p.approved_memberships), 
                    'unapproved_memberships': self.group_membership_data(p.unapproved_memberships)}
        except Exception, e:
            return {}
        
    def convert_cookie(self, cookie):
        sc = SimpleCookie()
        for key, value in cookie.iteritems():
            sc[key] = value
            
        return sc
    
    def get_user_data(self, user):
        cookies = request.cookies
        cookies = self.convert_cookie(cookies)
        
        #FIXME: get url from config and have standard fas object
        fas = ProxyClient('https://admin.fedoraproject.org/accounts')
        auth_params = {'cookie': cookies}
        result = fas.send_request('user/view/' + user, 
                                  auth_params = auth_params)
        print "**************", result
        
        if not result:
            return {}
        
        if len(result) > 1:
            p = result[1]['person']
        else:
            p = result[0]['person']
            
        return {'approved_memberships': self.group_membership_data(p['approved_memberships']), 
                'unapproved_memberships': self.group_membership_data(p['unapproved_memberships'])}

    def update_params(self, d):
        super(FedoraMembershipsToolWidget, self).update_params(d)
        
        resource_view = d.get('resourceview', None)
        if resource_view == 'profile_view':
            d.update(self.get_profile_data())
            print d
            return d
        
        person = d.get('person',d.get('data_key', None))
        if not person or person == tmpl_context.identity['person']['username']:
            d.update(self.get_profile_data())
            return d
        
        d.update(self.get_user_data(person))
        
        return d