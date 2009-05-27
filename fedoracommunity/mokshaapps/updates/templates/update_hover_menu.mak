  <div id="menu_@{request_id}" class="menu" panel="menu_panel_@{request_id}">
    % if show_package:
      <span class="package-name">
        <a href="/package_maintenance/tools/updates?package=@{name}" moksha_url="dynamic">@{name}</a>&nbsp;
      </span>
    % elif show_version:
      <span class="version">
        <a href="#"><strong>@{version}</strong></a>
      </span>
    % endif
            <div id="menu_panel_@{request_id}" class="menu_panel" >
            <h4>Quick Links for <strong>@{name}</strong>:</h4>
            <ul>
               <li><a href="https://admin.fedoraproject.org/updates/@{title}"><img src="/images/16_bodhi.png"/><span>Go to the @{title} <strong>update</strong> in Bodhi</span><img src="/images/16_offsite-link.png"/></a></li>
               <li><a href="http://koji.fedoraproject.org/koji/search?terms=@{nvr}&amp;type=build&amp;match=glob"><img src="/images/16_koji.png"/><span>Go to this <strong>build</strong> in Koji</span><img src="/images/16_offsite-link.png"/></a></li>
               <li><a href="https://admin.fedoraproject.org/pkgdb/packages/name/@{name}"><img src="/images/16_pkgdb.png"/><span>Go to @{name} <strong>package info</strong> in PackageDB</span><img src="/images/16_offsite-link.png"/></a></li>
               <li><a href="https://bugzilla.redhat.com/buglist.cgi?query_format=advanced&classification=Fedora&product=Fedora&component=@{name}&bug_status=NEW&bug_status=ASSIGNED&bug_status=MODIFIED"><img src="/images/16_bugzilla.png"/><span>Go to @{name} <strong>bugs</strong> in Bugzilla</span><img src="/images/16_offsite-link.png"/></a></li>
            </ul>
        </div>
      </div>
      <moksha_extpoint>
        {
            'type': 'make_menu',
            'placeholder_id': 'menu_@{request_id}',
            'id': '@{id}',
            'show_effect': 'slideDown(\"slow\")'
        }
      </moksha_extpoint>
