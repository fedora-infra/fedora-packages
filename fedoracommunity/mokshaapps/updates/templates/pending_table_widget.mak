<div class="list header-list">
    <table id="${id}">
        <thead>
            <tr>
                <th><a href="#nvr">Package</a></th>
                <th>Age</th>
                <th>Release(s)</th>
                <th>&nbsp;</th>
            </tr>
        </thead>
        <tbody class="rowtemplate">
            <tr>
                <td>
                  <div id="menu_@{id}" class="menu" panel="menu_panel_@{id}">
                    <span class="package-name">
                        <a href="/package_maintenance/tools/updates?package=@{name}">@{name}</a>&nbsp;
                    </span>
                            <div id="menu_panel_@{id}" class="menu_panel" >
                            <h4>Quick Links for <strong>@{name}</strong>:</h4>
                            <ul>
                               <li><a href="http://koji.fedoraproject.org/koji/buildinfo?buildID=@{id}"><img src="/images/16_koji.png"/><span>Go to this <strong>build</strong> in Koji</span><img src="/images/16_offsite-link.png"/></a></li>
                               <li><a href="https://admin.fedoraproject.org/updates/@{name}"><img src="/images/16_bodhi.png"/><span>Go to @{name} <strong>updates</strong> in Bodhi</span><img src="/images/16_offsite-link.png"/></a></li>
                               <li><a href="https://admin.fedoraproject.org/pkgdb/packages/name/@{name}"><img src="/images/16_pkgdb.png"/><span>Go to @{name} <strong>package info</strong> in PackageDB</span><img src="/images/16_offsite-link.png"/></a></li>
                               <li><a href="https://bugzilla.redhat.com/buglist.cgi?query_format=advanced&classification=Fedora&product=Fedora&component=@{name}&bug_status=NEW&bug_status=ASSIGNED&bug_status=MODIFIED"><img src="/images/16_bugzilla.png"/><span>Go to @{name} <strong>bugs</strong> in Bugzilla</span><img src="/images/16_offsite-link.png"/></a></li>
                               <li><a href="https://translate.fedoraproject.org/module/@{name}"><img src="/images/16_transifex.png"/><span>Go to @{name} <strong>translations</strong> in Transifex</span><img src="/images/16_offsite-link.png"/></a></li>
                            </ul>
                        </div>
                      </div>
                      <moksha_extpoint>
                        {
                            'type': 'make_menu',
                            'placeholder_id': 'menu_@{id}',
                            'id': '@{id}',
                            'show_effect': 'slideDown(\"slow\")'
                        }
                      </moksha_extpoint>
                    <div>@{versions}&nbsp;</div>
                </td>
                <td>@{date_submitted_display}</td>
                <td>@{releases}</td>
                <td>@{actions}</td>
            </tr>
        </tbody>
    </table>
    <div id="grid-controls">
        <div class="message template" id="info_display" >
           Viewing @{visible_rows} of @{total_rows} updates 
        </div>
        <div class="pager" id="pager" type="numeric" ></div>
        <div class="pager template" id="pager" type="more_link">
           <a href="@{more_link}" moksha_url="dynamic">View more pending updates &gt;</a>
        </div>
    </div>
</div>
