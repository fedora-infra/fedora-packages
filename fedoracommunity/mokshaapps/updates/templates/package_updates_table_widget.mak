<div class="list header-list">
    <div id="grid-controls">
        <form>
          <div id="filter" class="grid_filter" name="release_filter">
            <label for="release">Release:</label>
            <select name="release">
                <option selected="selected" value="">All Dists</option>
                % for (i, rel) in enumerate(release_table):
                    <option value="${rel['value']}">${rel['label']}</option>
                % endfor
            </select>
            <label for="status">Status:</label>
            <select name="status">
                <option selected="selected" value="">All</option>
                <option value="stable">Stable</option>
                <option value="testing">Testing</option>
                <option value="pending">Pending</option>
                <option value="obsolete">Obsolete</option>
            </select>
          </div>
        </form>
    </div>
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

    <div id="grid-controls" if="total_rows == 0">
        <div class="message template" id="info_display" >
           There are no updates for this package
        </div>
    </div>
    <div id="grid-controls" if="visible_rows < total_rows && total_rows != 0">
        <div class="message template" id="info_display" >
           Viewing all @{total_rows} updates for this package
        </div>
        <div class="pager template" id="pager" type="more_link">
           <a href="@{more_link}" moksha_url="dynamic">Goto updates &gt;</a>
        </div>
    </div>
    <div id="grid-controls" if="visible_rows < total_rows && total_rows != 0">
        <div class="message template" id="info_display" >
           Viewing @{first_visible_row}-@{last_visible_row} of @{total_rows} updates for this packahge
        </div>
        <div class="pager" id="pager" type="numeric" ></div>
        <div class="pager template" id="pager" type="more_link">
           <a href="@{more_link}" moksha_url="dynamic">View more updates &gt;</a>
        </div>
    </div>
</div>
