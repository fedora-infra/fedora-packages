from myfedora.widgets.resourceview import ToolWidget
from datetime import datetime
from tw.forms.datagrid import DataGrid
from myfedora.lib.app_factory import AppFactory
from myfedora.lib.utils import HRElapsedTime
from myfedora.lib.appbundle import AppBundle
import pylons
from tg import url
import koji

class BuildsToolApp(AppFactory):
    entry_name = 'tools.builds'

class BuildsToolWidget(ToolWidget):
    template = 'genshi:myfedora.plugins.apps.tools.templates.builds'
    display_name = "Builds"
    requires_data_key = False
    
    def update_params(self, d):
        super(ToolWidget, self).update_params(d)

        resourceview = d.get('resourceview', None)

        dk = d.get('data_key', None)
        person = d.get('person', None)
        profile = d.get('profile', None)
        package = d.get('package', None)
        username = None
        
        if resourceview == 'people_view':
            username = person
            
        elif resourceview == 'profile_view':
            profile = True

        left_col_apps = AppBundle("leftcol")
        build_table_class = pylons.g.apps['buildstable']
        build_table_app = build_table_class(None, 
                                            view='Canvas',
                                            person=person,
                                            package=package,
                                            profile=profile)
        left_col_apps.add(build_table_app)

        right_col_apps = AppBundle("rightcol")
        nav_class = pylons.g.apps['packagesnav']
        nav_app = nav_class(None, 
                            '320px', 
                            '200px', 
                            'Home',
                            flags=nav_class.BUILDS_SUBNAV_FLAG,
                            user=username,
                            package=package,
                            tool=d.get('tool','builds'))
        
        right_col_apps.add(nav_app)
        d.update({'rightcol': right_col_apps.serialize_apps(pylons.tmpl_context.w),
                  'leftcol': left_col_apps.serialize_apps(pylons.tmpl_context.w)
                  })

        return d
