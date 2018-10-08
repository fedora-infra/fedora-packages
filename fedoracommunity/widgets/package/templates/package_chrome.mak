<!-- START package chrome -->
<%
from urllib import quote
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

icon_url = tg.url("/images/icons/%s" % icon)
%>
<div class="bodycontent pb-3">
    <div class="subheader pb-2 clearfix">
      <div class="container pt-2">
      <img src="${icon_url}" class="package-image" height="96" width="96"/>
      <div class="package-header">
        <h2>${w.kwds['package_name']}
          <span class="dropdown show">
            <a class="btn btn-sm btn-secondary dropdown-toggle" href="#" id="dropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              ${w.kwds['package_name']} in other apps
            </a>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuLink">
              <a class="dropdown-item" href="https://admin.fedoraproject.org/updates/${w.package_info['name']}"><img src="${tg.url('/images/16_bodhi.png')}"/> Bodhi </a> </li>
              <a class="dropdown-item" href="https://bugzilla.redhat.com/buglist.cgi?component=${w.package_info['name']}&query_format=advanced&product=Fedora&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED"><img src = "https://admin.fedoraproject.org/community/images/16_bugs.png"/> Bugzilla </a>
              <a class="dropdown-item" href="https://retrace.fedoraproject.org/faf/problems/?component_names=${w.package_info['name']}"><img src = "${tg.url('/images/16_abrt.png')}"/> FAF </a>
              <a class="dropdown-item" href="http://koji.fedoraproject.org/koji/search?match=glob&type=package&terms=${quote(w.package_info['name'])}"><img src = "https://fedoraproject.org/static/images/icons/fedora-infra-icon_koji.png"/> Koji Builds </a>
              <a class="dropdown-item" href="https://src.fedoraproject.org/rpms/${w.package_info['name']}"><img src = "https://apps.fedoraproject.org/img/icons/git-logo.png" width=16px/> SCM </a>
            </div>
          </span>
        </h2>
        % if w.kwds['package_name'] != w.package_info['name']:
            Subpackage of <a class="subpackage_link" href="${tg.url('/%s' % w.package_info['name'])}">${w.package_info['name']}</a>
        % endif
        <div><em>${w.summary}</em></div>
      </div>
    </div>

    </div>

    <div id="tab-content">
     ${w.children[0].display(args=w.args, kwds=w.kwds) | n}
   </div>

</div>
<!-- END package chrome -->
