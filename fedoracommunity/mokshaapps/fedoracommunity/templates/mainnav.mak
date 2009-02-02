<div id="main_nav">
  <div id="app-sidebar">
    <div id="navigation_sidebar" class="nav">
<ul id="${id}">
  % for t in tabs:
    <li><a href="${t['url']}" title="${t['label']} Page">
                    ${t['label']}
                </a></li>
    
  % endfor
</ul>
    </div>
  </div>

<div id="content">
            % for t in tabs:
    <div id="${t['label']}_Page"></div>
  % endfor
    <div class="clearingdiv"></div>
 </div>
</div>