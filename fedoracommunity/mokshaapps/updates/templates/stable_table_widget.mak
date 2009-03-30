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
                    <span class="package-name">
                        <a href="javascript:moksha.goto('/package_maint/package/updates', {'package': '@{name}'})">@{name}</a>&nbsp;
                    </span>
                    <div>@{versions}&nbsp;</div>
                </td>
                <td>@{date_pushed_display:index("date")}</td>
                <td>@{releases}</td>
            </tr>
        </tbody>
    </table>
</div>
