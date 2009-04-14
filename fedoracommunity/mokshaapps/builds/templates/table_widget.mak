    <div class="list header-list">
        <table id="${id}">
            <thead>
                <tr>
                    <th><a href="#nvr">Package</a></th>
                    <th><a href="#owner_name">Built By</a></th>
                    <th>Build Time</th>
                    <th>Finished</th>
                    <th><a href="#state">Status</a></th>
                    <th>&nbsp;</th>
                </tr>
            </thead>
            <tbody class="rowtemplate">
                    <tr>
                        <td class="one-row">
                          <div id="menu_@{build_id}" class="menu" panel="menu_panel_@{build_id}">
                            <span class="package-name">
                                <a href="javascript:moksha.goto('/package_maintenance/packages/builds', {'package': '@{package_name}'});">@{package_name}</a>
                            </span>
                            <br/>@{version}&nbsp;
                            <div id="menu_panel_@{build_id}" class="menu_panel">
                            <ul>
                               <li>
                                 <a target="_blank" href="http://koji.fedoraproject.org/koji/buildinfo?buildID=@{build_id}">
                                   View this build in Koji
                                 </a>
                                 <a target="_blank" href="https://admin.fedoraproject.org/updates/@{package_name}">
                                   View updates for this package in Bodhi
                                 </a>
                                 <a target="_blank" href="https://admin.fedoraproject.org/pkgdb/packages/name/@{package_name}">
                                   View this package in PackageDB
                                 </a>
                                 <a target="_blank" href="https://translate.fedoraproject.org/module/@{package_name}">
                                   View translations this package in Transifex
                                 </a>
                               </li>
                            </ul>
                            </div>
                          </div>
                          <moksha_extpoint>
                            {
                                'type': 'make_menu',
                                'placeholder_id': 'menu_@{build_id}',
                                'build_id': '@{build_id}',
                                'show_effect': 'slideDown(\"slow\")'
                            }
                          </moksha_extpoint>
                        </td>

                        <td rowspan="2">
                            <span class="person-name"><a href="javascript:moksha.goto('/people/', {'username': '@{owner_name}'})">@{owner_name}</a></span>&nbsp;
                        </td>
                        <td rowspan="2">@{completion_time_display:index("elapsed")}
                        </td>
                        <td rowspan="2">@{completion_time_display:index("when")}
                            <br/>
                               @{completion_time_display:index("time")}
                        </td>

                        <td rowspan="2"><img src="/images/16_build_state_@{state}.png" /></td>
                        <td rowspan="2" id="@{release_id}">
                            &nbsp;
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


    </div>
