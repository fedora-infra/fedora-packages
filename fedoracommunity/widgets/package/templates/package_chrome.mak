<!-- START package chrome -->
<div id="container">
    <div class="container_24">
         <div class="grid_5" id="package-info-bar">
             <img src="/images/package_128x128.png" height="128" width="128"/>
             <div>
                 <div><h3>LATEST BUILD</h3></div>
                 <div class="package-name">${latest_build}</div>
             </div>
             <br />
             <div>
                 <div><h3>PACKAGE TREE</h3></div>
                 <ul>
                   <li><a class="package-name" href="/${kwds['package_name']}">${kwds['package_name']}</a>
                   <ul>
                       % for subpkg in package_info['sub_pkgs']:
                             <li><a class="package-name" href="${subpkg['name']}">${subpkg['name']}</a></li>
                       % endfor
                   </ul>
                 </li>
                 </ul>
             </div>
         </div>
         <div class="grid_19" id="package-header">
             <h2>${kwds['package_name']}</h2>
             <div><em>${package_info['summary']}</em></div>
             <div>${widget(args=args, kwds=kwds) | n}</div>
         </div>
         <div class="clear"></div>
    </div>
</div>
<!-- END package chrome -->
