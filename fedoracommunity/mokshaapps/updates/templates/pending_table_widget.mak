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
                    <span class="package-name">
                        <a href="/package_maintenance/tools/updates?package=@{name}">@{name}</a>&nbsp;
                    </span>
                    <div>@{versions}&nbsp;</div>
                </td>
                <td>@{date_submitted_display:index("when")}</td>
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
