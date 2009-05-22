<div class="list header-list">
    <table id="${id}">
        <thead>
            <tr>
                <th><a href="#nvr">Version</a></th>
                <th>Age</th>
                <th>Status</th>
                <th>&nbsp;</th>
            </tr>
        </thead>
        <tbody class="rowtemplate">
            <tr class="@{status}-update @{type}-update">
                <td>
                  ${c.update_hover_menu(show_package=False, show_version=True)}
                </td>
                <td>@{date_pushed_display}</td>
                <td>@{status}
                    <div class="karma"><a href="https://admin.fedoraproject.org/updates/@{title}" moksha_url="dynamic"><img src="/images/16_karma-@{karma_level}.png" />@{karma_str} karma</a></div>
                </td>
                <td>
                  @{details}
                </td>
            </tr>
        </tbody>
    </table>
    <div id="grid-controls">
        <div class="message template" id="info_display" >
           Viewing @{visible_rows} of @{total_rows} updates
        </div>
        <div class="pager" id="pager" type="numeric" ></div>
        <div class="pager template" id="pager" type="more_link">
           <a href="@{more_link}" moksha_url="dynamic">View more stable updates &gt;</a>
        </div>
    </div>
</div>
