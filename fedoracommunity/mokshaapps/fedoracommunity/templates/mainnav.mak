<div id="main_nav">
 <div id="${id}">
  <div id="app-sidebar">
    <div id="navigation_sidebar" class="nav">
      ${tabwidget(root_id=root_id, tabs=tabs) | n}
    </div>
  </div>

  <div id="content">
    ${panewidget(root_id=root_id, tabs=tabs) | n}
  </div>
 </div>
</div>
