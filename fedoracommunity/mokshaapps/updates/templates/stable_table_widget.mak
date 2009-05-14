<div class="list header-list">
    <table id="${id}">
        <thead>
            <tr>
                <th><a href="#nvr">Package</a></th>
                <th>Date Pushed to Stable</th>
                <th>Release(s)</th>
            </tr>
        </thead>
        <tbody class="rowtemplate">
            <tr>
                <td>
                    ${c.update_hover_menu()}
                    <div>@{versions}&nbsp;</div>
                </td>
                <td>@{date_pushed}</td>
                <td>@{releases}</td>
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
