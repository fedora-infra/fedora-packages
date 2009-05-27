<div class="list header-list">
        <div id="grid-controls">
            <div class="alpha-pager pager" id="pager" type="alpha" ></div>
        </div>
        <table id="${id}">
            <thead>
                <tr>
                    <th>Package</th>
                </tr>
            </thead>
            <tbody class="rowtemplate">
                    <tr>
                        <td>
                            <span class="package-name">
                                <a href="/package_maintenance?package=@{name}" moksha_url="dynamic">@{name}</a>
                            </span>
                        </td>
                    </tr>
            </tbody>
        </table>
        <div id="grid-controls">
            <div class="message template" id="info_display" >
               Viewing @{first_visible_row}-@{last_visible_row} of @{total_rows} packages
            </div>
            <div class="pager" id="pager" type="numeric" ></div>
            <div class="pager template" id="pager" type="more_link">
               <a href="@{more_link}" moksha_url="dynamic">View more packages &gt;</a>
            </div>
        </div>
</div>

