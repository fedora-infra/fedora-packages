<!-- this is the beginning of people_package_nav.mak -->
 <div id="${id}">
   <div class="header-content-column">
     % if not profile:
              <script type="text/javascript">
                  moksha.update_title("User: ${username}", 2);
              </script>
     % endif

     <h2>${human_name}</h2>
     % if error:
        ${error}
     % else:
   </div>
   <div class="right-content-column">
     <div class="panel">
     <h3>Package Maintenance</h3>
     ${tabwidget(root_id=root_id, tabs=tabs)}
     </div>
     ${applist_widget(category=sidebar_apps)}
     <div id="clear"></div>
   </div>
   <div class="left-content-column">
     ${applist_widget(category=header_apps)}
     ${panewidget(root_id=root_id, tabs=tabs)}
     % endif
   </div>
 </div>
<!-- this is the end of people_package_nav.mak -->
