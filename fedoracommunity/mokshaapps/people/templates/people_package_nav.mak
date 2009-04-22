<!-- this is the beginning of people_package_nav.mak -->
 <div id="${id}">
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
   </div>
 </div>
<!-- this is the end of people_package_nav.mak -->
