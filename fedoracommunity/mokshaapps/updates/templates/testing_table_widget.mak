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
          </div>
        </form>
    </div>
    <script type="text/javascript">
        function _render_br_list(list) {
            result = list
            if (typeof(list) != 'string' && list.join)
                result = list.join('<br />');

            return result;
        }
    </script>
    <table id="${id}">
        <thead>
            <tr>
                <th><a href="#nvr">Package</a></th>
                <th>Age</th>
                <th>Release(s)</th>
                <th>Status</th>
                <th>&nbsp;</th>
            </tr>
        </thead>

        <tbody class="rowtemplate">
            <tr>
                <td>
                    ${c.update_hover_menu()}
                    <div>@{versions:filter(_render_br_list)}&nbsp;</div>
                </td>
                <td>@{date_pushed_display}</td>
                <td><br/>@{releases:filter(_render_br_list)}</td>
                <td><span>@{status}</span>
                <div class="karma"><a href="https://admin.fedoraproject.org/updates/@{title}"><img src="/images/16_karma-@{karma_level}.png" />@{karma_str} karma</a></div>
                </td>
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
           <a href="@{more_link}" moksha_url="dynamic">View more testing updates &gt;</a>
        </div>
    </div>
</div>
