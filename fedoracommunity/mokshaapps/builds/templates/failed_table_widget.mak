    <div class="list header-list">
        <table id="${id}" class="${table_class}">
            <thead>
                <tr>
                    <th><a href="#nvr">Package</a></th>
                    <th>Failed</th>
                    % if not profile:
                        <th>Built By</th>
                    % endif
                </tr>
            </thead>

            <tbody class="rowtemplate">
                    <tr class="failed-build">
                        <td class="one-row">
                          <div id="menu_@{build_id}" class="menu" panel="menu_panel_@{build_id}">
                            <span class="package-name">
                                <a href="/package_maintenance/tools/builds?package=@{package_name}" moksha_url="dynamic">@{package_name} <img src="/images/16_hover_bubble.png" alt="" /></a>
                            </span>
                            <br/>@{version}-@{release}&nbsp;
                            <div id="menu_panel_@{build_id}" class="menu_panel" >
<div id='items_@{build_id}'>
<h4>Quick Links for <strong>@{package_name}</strong>:</h4>
                            <ul>
                               <li><a href="http://koji.fedoraproject.org/koji/buildinfo?buildID=@{build_id}"><img src="/images/16_koji.png"/><span>Go to this <strong>build</strong> in Koji</span><img src="/images/16_offsite-link.png"/></a></li>
                               <li><a href="https://admin.fedoraproject.org/updates/@{package_name}"><img src="/images/16_bodhi.png"/><span>Go to @{package_name} <strong>updates</strong> in Bodhi</span><img src="/images/16_offsite-link.png"/></a></li>
                               <li><a href="https://admin.fedoraproject.org/pkgdb/packages/name/@{package_name}"><img src="/images/16_pkgdb.png"/><span>Go to @{package_name} <strong>package info</strong> in PackageDB</span><img src="/images/16_offsite-link.png"/></a></li>
                               <li><a href="https://bugzilla.redhat.com/buglist.cgi?query_format=advanced&classification=Fedora&product=Fedora&component=@{package_name}&bug_status=NEW&bug_status=ASSIGNED&bug_status=MODIFIED"><img src="/images/16_bugzilla.png"/><span>Go to @{package_name} <strong>bugs</strong> in Bugzilla</span><img src="/images/16_offsite-link.png"/></a></li>
                               <!-- <li><a href="https://translate.fedoraproject.org/module/@{package_name}"><img src="/images/16_transifex.png"/><span>Go to @{package_name} <strong>translations</strong> in Transifex</span><img src="/images/16_offsite-link.png"/></a></li> -->
                            </ul>
<h4>Changelog</h4>
<div class="changelog">
                <moksha_extpoint>
                                {
                                    'type': 'make_menu',
                                    'placeholder_id': 'menu_@{build_id}',
                                    'build_id': '@{build_id}',
                                    'show_effect': 'slideDown(\"slow\")'
                                }
                            </moksha_extpoint>
                <moksha_extpoint>
                                {
                                    'type': 'build_menu',
                                    'placeholder_id': 'items_@{build_id}',
                                    'menu_id': 'menu_@{build_id}',
                                    'build_id': '@{build_id}',
                                    'task_id': '@{task_id}',
                                    'build_state': @{state},
                                    'show_effect': 'slideDown(\"slow\")'
                                }
                            </moksha_extpoint>
</div>
                                                        </div>
                                                 </td>

                        <td rowspan="2">@{completion_time_display:index("when")}
                        </td>

                        % if not profile:
                        <td rowspan="2">
                            <span class="person-name"><a href="/people/?username=@{owner_name}" moksha_url="dynamic">@{owner_name}</a></span>&nbsp;
                        </td>
                        % endif
                    </tr>
                    <tr class="failed-build">
                        <td colspan="6"
                            id="message_@{build_id}"
                            class="message_row">
                            <moksha_extpoint>
                            {
                                'type': 'build_message',
                                'placeholder_id': 'message_@{build_id}',
                                'build_id': '@{build_id}',
                                'task_id': '@{task_id}',
                                'build_state': @{state},
                                'show_effect': 'slideDown(\"slow\")'
                            }
                            </moksha_extpoint>

                        </td>
                    </tr>
                </tbody>
        </table>
        <div id="grid-controls" if="total_rows == 0">
            <div class="message template" id="info_display" >
                No failed builds found.
            </div>
        </div>
        <div id="grid-controls" if="visible_rows >= total_rows && total_rows != 0">
            <div class="message template" id="info_display" >
               Viewing all failed builds
            </div>

            <div class="pager template" id="pager" type="more_link">
               <a href="@{more_link}" moksha_url="dynamic">Goto failed builds &gt;</a>
            </div>
        </div>
        <div id="grid-controls" if="visible_rows < total_rows">
            <div class="message template" id="info_display" >
               Viewing @{first_visible_row}-@{last_visible_row} of @{total_rows} failed builds
            </div>
            <div class="pager" id="pager" type="numeric" ></div>
            <div class="pager template" id="pager" type="more_link">
               <a href="@{more_link}" moksha_url="dynamic">View more failed builds &gt;</a>
            </div>
        </div>
    </div>
