<!-- START package chrome -->
<%
import tg

icon = w.package_info['icon']
if w.package_name != w.package_info['name']:
    # subpackage
    for sub_pkg in w.package_info['sub_pkgs']:
        if sub_pkg['name'] == w.package_name:
            sub_icon = sub_pkg.get('icon', None)
            if sub_icon:
                icon = sub_icon

            break

icon_url = tg.url("/images/icons/%s.png" % icon)
%>
<div id="container">
    <div class="container_24" id="package-details">
         <div class="grid_5" id="package-info-bar">
             <img src="${icon_url}" height="128" width="128"/>
             <div class="build">
                 <div><h3>LATEST BUILD</h3></div>
                 <div class="package-name">${w.latest_build}</div>
             </div>

             <div class="owner">
                 <div><h3>OWNER</h3></div>
                 % if w.package_info.get('devel_owner', None):
                     <div class="package-owner">${w.package_info['devel_owner']}</div><div class="package-dist">(Rawhide)</div>
                 % else:
                     <div class="package-owner orphan">Orphaned</div><div class="package-dist">(Rawhide)</div>
                 % endif
             </div>
             <div class="package-tree">
                 <div><h3>PACKAGE TREE</h3></div>
                 <ul>
                   <li><a class="package-name" href="${tg.url('/%s' % w.package_info['name'])}">${w.package_info['name']}</a>
                   <ul>
                       % for subpkg in w.package_info['sub_pkgs']:
                             <li><a class="package-name" href="${tg.url('/%s' % subpkg['name'])}">${subpkg['name']}</a></li>
                       % endfor
                   </ul>
                 </li>
                 </ul>
             </div>
         </div>
         <div class="grid_19">
           <div id="package-header">
             <h2>${w.kwds['package_name']}</h2>
             % if w.kwds['package_name'] != w.package_info['name']:
                 Subpackage of <a class="subpackage_link" href="${tg.url('/%s' % w.package_info['name'])}">${w.package_info['name']}</a>
             % endif
             <div><em>${w.summary}</em></div>
           </div>
           <div id="tab-content">
            ${w.children[0].display(args=w.args, kwds=w.kwds) | n}
          </div>
         </div>
         <div class="clear"></div>
    </div>
</div>
<!-- END package chrome -->
