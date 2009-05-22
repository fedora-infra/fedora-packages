
    <div class="list header-list">
        <div id="grid-controls">
            <div class="alpha-pager pager" id="pager" type="alpha" ></div>
        </div>
        <table id="${id}">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Username</th>
                </tr>
            </thead>
            <tbody class="rowtemplate">
                    <tr>
                        <td>
                            <span class="person-name">
                                <a href="/people?username=@{username}" moksha_url="dynamic">@{human_name}</a>
                            </span>

                        <td>
                            <span class="person-name"><a href="/people?username=@{username}" moksha_url="dynamic">@{username}</a></span>&nbsp;
                        </td>
                </tbody>

        </table>
        <div id="grid-controls">
            <div class="message template" id="info_display" >
               Viewing @{first_visible_row}-@{last_visible_row} of @{total_rows} people
            </div>
            <div class="pager" id="pager" type="numeric" ></div>
        </div>
    </div>
