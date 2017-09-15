<% import tg %>
<html>
<head></head>
<body>
<div class="list header-list">
    <div id="grid-controls" class="text-xs-right pb-1">
        <form>
          <div id="filter" class="grid_filter" name="release_filter">
            <label for="release">Release:</label>
            <select name="release" class="custom-select">
                <option selected="selected" value="">All Dists</option>
                % for (i, rel) in enumerate(w.release_table):
                    <option value="${rel['value']}">${rel['label']}</option>
                % endfor
            </select>
            <label for="status">Status:</label>
            <select name="status" class="custom-select">
                <option selected="selected" value="">All</option>
                <option value="stable">Stable</option>
                <option value="testing">Testing</option>
                <option value="pending">Pending</option>
                <option value="obsolete">Obsolete</option>
            </select>
            <input type="hidden" name="group_updates" value="False"/>
          </div>
        </form>
    </div>
    <table id="${w.id}" class="table">
        <thead>
            <tr>
                <th><a href="#nvr">Version</a></th>
                <th>Age</th>
                <th>Status</th>
                <th>&nbsp;</th>
            </tr>
        </thead>
        <tbody class="rowtemplate">
            <tr class="${'${status}'}-update ${'${type}'}-update">
                <td>
                  {{html render_update_builds(title)}}
                </td>
                <td>${'${date_pushed_display}'}</td>
                <td>${'${status}'}
                    <div class="karma_${'${karma_level}'}">
                        <a href="https://admin.fedoraproject.org/updates/${'${title}'}" moksha_url="static">
                            <img src="${tg.url('/images/16_karma-${karma_level}.png')}" />${'${karma_str}'} karma
                        </a>
                    </div>
                </td>
                <td>
                  {{html details}}
                </td>
            </tr>
        </tbody>
    </table>

    <div id="grid-controls" if="total_rows == 0">
        <div class="message template" id="info_display" >
           There are no updates for this package
        </div>
    </div>
    <div id="grid-controls" if="visible_rows > total_rows && total_rows > 0">
        <div class="message template" id="info_display" >
           Viewing all ${'${total_rows}'} updates for this package
        </div>
    </div>
    <div id="grid-controls" if="visible_rows > total_rows && total_rows > 0">
        <div class="message template" id="info_display" >
           Viewing ${'${first_visible_row}'}-${'${last_visible_row}'} of ${'${total_rows}'} updates for this packahge
        </div>
        <div class="pager" id="pager" type="numeric" ></div>
    </div>
</div>
</body>
</html>
