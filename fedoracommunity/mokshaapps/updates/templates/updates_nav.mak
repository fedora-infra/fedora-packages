<div id="sidebar-nav">
 <div id="${id}">
   <div class="right-content-column">
     <div class="app panel">
       <h3>Updates</h3>
       ${tabwidget(root_id=root_id, tabs=tabs)}
     </div>
     <div class="panel">
     ${applist_widget(category=sidebar_apps)}
     </div>
     <div id="clear"></div>
   </div>
   <div class="left-content-column">
     ${panewidget(root_id=root_id, tabs=tabs)}
   </div>
 </div>
</div>
