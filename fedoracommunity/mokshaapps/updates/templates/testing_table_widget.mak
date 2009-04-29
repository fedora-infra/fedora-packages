<div class="list header-list">
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
                    <span class="package-name">
                        <a href="/package_maintenance/tools/updates?package=@{name}">@{name}</a>&nbsp;
                    </span>
                    <div>@{versions}&nbsp;</div>
                </td>
                <td>@{date_pushed_display:index("when")}</td>
                <td>@{releases}</td>
                <td><span>@{status}</span>
                    <div><img src="/images/16_karma-@{karma_level}.png" />@{karma_str} karma</div>
                </td>
                <td>@{actions}</td>
            </tr>
        </tbody>
    </table>
</div>
