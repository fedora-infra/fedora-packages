<div id="content-nav">
<ul id="${id}">
  % for t in tabs:
    <li><a href="${t['url']}" title="${t['label']} Page">
                    ${t['label']}
                </a></li>
    
  % endfor
</ul>
  % for t in tabs:
    <div id="${t['label']}_Page"></div>
    
  % endfor
</div>