<div class="list header-list">
    <table id="${id}">
        <thead>
            <tr>
                <th><a href="#nvr">Package</a></th>
                <th>Age</th>
                <th>Date Pushed</th>
                <th>Release(s)</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody class="rowtemplate">
            <tr>
                <td>
                    <span class="package-name">
                        @{name}&nbsp;
                    </span>
                    <div>@{version_str}&nbsp;</div>
                </td>
                <td>@{date_pushed_display:index("when")}</td>
                <td>@{date_pushed_display:index("date")}</td>
                <td>@{release_label}</td>
                <td><span>@{status}</span>
                    <div><img src="/images/16_karma-@{karma_level}.png" />@{karma_str} karma</div>
                </td>
            </tr>
        </tbody>
    </table>
</div>
