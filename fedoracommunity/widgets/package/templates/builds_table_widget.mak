<% import tg %>
<html>
<head></head>
<body>
    <div class="list header-list">
        <div id="grid-controls" class="text-xs-right pb-1">
            <form>
              <div id="filter" class="grid_filter" name="status_filter">

                <label for="state">Status:</label>
                <select name="state" class="custom-select custom-select-sm">
                    <option selected="selected" value="">All</option>
                    <option value="0" style="background:url(${tg.url('/images/16_build_state_0.png')}) no-repeat center left; padding-left: 18px;"></img>Building</option>
                    <option value="1" style="background:url(${tg.url('/images/16_build_state_1.png')}) no-repeat center left; padding-left: 18px;">Success</option>
                    <option value="3" style="background:url(${tg.url('/images/16_build_state_3.png')}) no-repeat center left; padding-left: 18px;">Failed</option>
                    <option value="4" style="background:url(${tg.url('/images/16_build_state_4.png')}) no-repeat center left; padding-left: 18px;">Canceled</option>
                    <option value="2" style="background:url(${tg.url('/images/16_build_state_2.png')}) no-repeat center left; padding-left: 18px;">Deleted</option>
                </select>
              </div>
            </form>
        </div>
        <table id="${w.id}" class="table">
            <thead>
                <tr>
                    <th>Package</th>
                    <th>When</th>
                    <th>Build Time</th>
                    <th>Built By</th>
                </tr>
            </thead>

            <tbody class="rowtemplate">
                    <tr>
                        <td class="one-row">
                          <div id="menu_${'${build_id}'}" class="menu" panel="menu_panel_${'${build_id}'}">
                            <span class="package-name">
                                <% icon = tg.url("/images/16_build_state_${state}.png") %>
                                <img src="${icon}"></img>
                            </span>
                            <a href="http://koji.fedoraproject.org/koji/buildinfo?buildID=${'${build_id}'}">${'${package_name}'}-${'${version}'}-${'${release}'}</a>&nbsp;
                            <div id="menu_panel_${'${build_id}'}" class="menu_panel" >
<div id="items_${'${build_id}'}">
<h4>Quick Links for <strong>${'${package_name}'}</strong>:</h4>
                            <ul>
                               <li><a href="http://koji.fedoraproject.org/koji/buildinfo?buildID=${'${build_id}'}"><img src="${tg.url('/images/16_koji.png')}"/><span>Go to this <strong>build</strong> in Koji</span><img src="${tg.url('/images/16_offsite-link.png')}"/></a></li>
                               <li><a href="https://admin.fedoraproject.org/updates/${'${package_name}'}" moksha_url="dynamic"><img src="${tg.url('/images/16_bodhi.png')}"/><span>Go to ${'${package_name}'} <strong>updates</strong> in Bodhi</span><img src="${tg.url('/images/16_offsite-link.png')}"/></a></li>
                               <li><a href="https://admin.fedoraproject.org/pkgdb/package/${'${package_name}'}" moksha_url="dynamic"><img src="${tg.url('/images/16_pkgdb.png')}"/><span>Go to ${'${package_name}'} <strong>package info</strong> in PackageDB</span><img src="${tg.url('/images/16_offsite-link.png')}"/></a></li>
                               <li><a href="https://bugzilla.redhat.com/buglist.cgi?query_format=advanced&classification=Fedora&product=Fedora&component=${'${package_name}'}&bug_status=NEW&bug_status=ASSIGNED&bug_status=MODIFIED"><img src="${tg.url('/images/16_bugzilla.png')}"/><span>Go to ${'${package_name}'} <strong>bugs</strong> in Bugzilla</span><img src="${tg.url('/images/16_offsite-link.png')}"/></a></li>
                               <!-- <li><a href="https://translate.fedoraproject.org/module/@{package_name}"><img src="${tg.url('/images/16_transifex.png')}"/><span>Go to ${'${package_name}'} <strong>translations</strong> in Transifex</span><img src="${tg.url('/images/16_offsite-link.png')}"/></a></li> -->
                            </ul>
                              <h4>Changelog</h4>
                              <div class="changelog">
                                <div class="moksha_extpoint">
                        	    {
                        	        'type': 'make_menu',
                        	        'placeholder_id': "menu_${'${build_id}'}",
                        	        'build_id': "${'${build_id}'}",
                        	        'show_effect': 'slideDown(\"slow\")'
                        	    }
                        	</div>
                                <div class="moksha_extpoint">
                                {
                                    'type': 'build_menu',
                                    'placeholder_id': "items_${'${build_id}'}",
                                    'menu_id': "menu_${'${build_id}'}",
                                    'build_id': "${'${build_id}'}",
                                    'task_id': "${'${task_id}'}",
                                    'build_state': ${'${state}'},
                                    'show_effect': 'slideDown(\"slow\")'
                                }
                          	</div>
                               </div>
                             </div>
                        </td>

                        <td rowspan="2">${'${completion_time_display["when"]}'}
                        </td>

                        <td rowspan="2">${'${completion_time_display["elapsed"]}'}
                        </td>

                        <td rowspan="2">
                            <span class="person-name">${'${owner_name}'}</a></span>&nbsp;
                        </td>
                    </tr>
                    <tr>
                        <td colspan="6"
                            id="message_${'${build_id}'}"
                            class="message_row">
                            <div class="moksha_extpoint">
                            {
                                'type': 'build_message',
                                'placeholder_id': "message_${'${build_id}'}",
                                'build_id': "${'${build_id}'}",
                                'task_id': "${'${task_id}'}",
                                'build_state': "${'${state}'}",
                                'show_effect': 'slideDown(\"slow\")'
                            }
                            </div>

                        </td>
                    </tr>
                </tbody>
        </table>
        <div id="grid-controls" if="total_rows == 0">
            <div class="message template" id="info_display" >
                No builds currently in-progress.
            </div>
        </div>
        <div id="grid-controls" if="visible_rows >= total_rows && total_rows != 0">
            <div class="message template" id="info_display" >
               Viewing all current builds
            </div>
        </div>
        <div id="grid-controls" if="visible_rows < total_rows">
            <div class="message template" id="info_display" >
               Viewing ${'${first_visible_row}'}-${'${last_visible_row}'} of ${'${total_rows}'} builds
            </div>
            <div class="pager" id="pager" type="numeric" ></div>
        </div>
    </div>
</body>
</html>
