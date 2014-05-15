<!-- START package chrome -->
<%
import tg

icon = w.package_info['icon']
package_name = w.kwds['package_name']
if package_name != w.package_info['name']:
    # subpackage
    for sub_pkg in w.package_info['sub_pkgs']:
        if sub_pkg['name'] == package_name:
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
                     % if w.package_info['devel_owner'].endswith('-maint'):
                         <div class="package-owner"><a class="package-owner" href="https://admin.fedoraproject.org/pkgdb/users/packages/${w.package_info['devel_owner']}">${w.package_info['devel_owner']}</a></div><div class="package-dist">(Rawhide)</div>
                     % else:
                         <div class="package-owner"><a class="package-owner" href="https://fedoraproject.org/wiki/User:${w.package_info['devel_owner']}">${w.package_info['devel_owner']}</a></div><div class="package-dist">(Rawhide)</div>
                     % endif
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
             <div class="other-app">
		 <h3> In other apps </h3>
                 <ul>
	           <li><a class="other-app" href="https://admin.fedoraproject.org/updates/${w.package_info['name']}"><img src ="https://admin.fedoraproject.org/community/images/16_bodhi.png"/> Bodhi </a> </li>
                   <li><a class="other-app" href="http://koji.fedoraproject.org/koji/search?match=glob&type=package&terms=${w.package_info['name']}"><img src = "https://fedoraproject.org/static/images/icons/fedora-infra-icon_koji.png"/> Koji Builds </a> </li>
                   <li><a class="other-app" href="https://bugzilla.redhat.com/buglist.cgi?component=${w.package_info['name']}&query_format=advanced&product=Fedora&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED"><img src = "https://admin.fedoraproject.org/community/images/16_bugs.png"/> Bugzilla </a> </li>
                   <li><a class="other-app" href="http://pkgs.fedoraproject.org/cgit/${w.package_info['name']}.git"><img src = "https://apps.fedoraproject.org/img/icons/git-logo.png"/> SCM </a> </li>
                   <li><a class="other-app" href="https://admin.fedoraproject.org/pkgdb/package/${w.package_info['name']}"><img src = "https://fedoraproject.org/static/images/icons/fedora-infra-icon_pkgdb.png"/> Pkgdb Package Info </a></li>
                   <li><a class="other-app" href="https://apps.fedoraproject.org/tagger/${w.package_info['name']}"><img src = "${tg.url('/images/16_tagger.png')}"/> Tagger </a></li>
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
