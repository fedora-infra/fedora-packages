<div class="list header-list">
    <table id="${id}">
        <thead>
            <tr>
                <th><a href="#nvr">Package</a></th>
                <th>Age</th>
                <th>Release(s)</th>
                <th></th>
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
                <td>@{date_submitted_display:index("when")}</td>
                <td>@{releases}</td>
                <td>@{actions}</td>
            </tr>
        </tbody>
    </table>
</div>
