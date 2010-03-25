    <div class="list header-list">
        <table id="${id}" class="${table_class}">
            <thead>
                <tr>
                    <th><a href="#nvr">Package</a></th>
                    <th>Build Time</th>
                    <th>Finished</th>
                    % if not profile:
                        <th><a href="#owner_name">Built By</a></th>
                    % endif
                    <th>&nbsp;</th>
                </tr>
            </thead>

            <tbody class="rowtemplate">
                    <tr>
                        <td class="one-row">
                          <div id="menu_@{build_id}" class="menu" panel="menu_panel_@{build_id}">
                            <span class="package-name">
                                <a href="/package_maintenance/tools/builds?package=@{package_name}" moksha_url="dynamic">@{package_name} </a>
                            </span>
                            <br/>@{version}-@{release}&nbsp;
                            <div id="menu_panel_@{build_id}" class="menu_panel" >
<div id='items_@{build_id}'>
<h4>Quick Links for <strong>@{package_name}</strong>:</h4>
                            <ul>
                               <li><a href="http://koji.fedoraproject.org/koji/buildinfo?buildID=@{build_id}"><img src="${tmpl_context.get_url('/images/16_koji.png')}"/><span>Go to this <strong>build</strong> in Koji</span><img src="${tmpl_context.get_url('/images/16_offsite-link.png')}"/></a></li>
                               <li><a href="https://admin.fedoraproject.org/updates/@{package_name}" moksha_url="dynamic"><img src="${tmpl_context.get_url('/images/16_bodhi.png')}"/><span>Go to @{package_name} <strong>updates</strong> in Bodhi</span><img src="${tmpl_context.get_url('/images/16_offsite-link.png')}"/></a></li>
                               <li><a href="https://admin.fedoraproject.org/pkgdb/acls/name/@{package_name}" moksha_url="dynamic"><img src="${tmpl_context.get_url('/images/16_pkgdb.png')}"/><span>Go to @{package_name} <strong>package info</strong> in PackageDB</span><img src="${tmpl_context.get_url('/images/16_offsite-link.png')}"/></a></li>
                               <li><a href="https://bugzilla.redhat.com/buglist.cgi?query_format=advanced&classification=Fedora&product=Fedora&component=@{package_name}&bug_status=NEW&bug_status=ASSIGNED&bug_status=MODIFIED"><img src="${tmpl_context.get_url('/images/16_bugzilla.png')}"/><span>Go to @{package_name} <strong>bugs</strong> in Bugzilla</span><img src="${tmpl_context.get_url('/images/16_offsite-link.png')}"/></a></li>
                               <!-- <li><a href="https://translate.fedoraproject.org/module/@{package_name}"><img src="${tmpl_context.get_url('/images/16_transifex.png')}"/><span>Go to @{package_name} <strong>translations</strong> in Transifex</span><img src="${tmpl_context.get_url('/images/16_offsite-link.png')}"/></a></li> -->
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

                        <td rowspan="2">@{completion_time_display:index("elapsed")}
                        </td>
                        <td rowspan="2">@{completion_time_display:index("when")}
                            <br/>
                               @{completion_time_display:index("time")}
                        </td>
                        % if not profile:
                        <td rowspan="2">
                            <span class="person-name"><a href="/people/?username=@{owner_name}" moksha_url="dynamic">@{owner_name}</a></span>&nbsp;
                        </td>
                        % endif

                        <td rowspan="2" id="@{release_id}">
                            &nbsp;
                            <div class="update_details">
                               @{update_details}
                            </div>
                        </td>
                    </tr>
                    <tr>
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
                No builds found.
            </div>
        </div>
        <div id="grid-controls" if="visible_rows >= total_rows && total_rows != 0">
            <div class="message template" id="info_display" >
               Viewing all builds
            </div>

            <div class="pager template" id="pager" type="more_link">
               <a href="@{more_link}" moksha_url="dynamic">Goto builds &gt;</a>
            </div>
        </div>
        <div id="grid-controls" if="visible_rows < total_rows">
            <div class="message template" id="info_display" >
               Viewing @{first_visible_row}-@{last_visible_row} of @{total_rows} builds
            </div>
            <div class="pager" id="pager" type="numeric" ></div>
            <div class="pager template" id="pager" type="more_link">
               <a href="@{more_link}" moksha_url="dynamic">View more builds &gt;</a>
            </div>
        </div>
    </div>
